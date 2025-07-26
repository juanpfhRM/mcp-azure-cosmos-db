import fs from 'fs';
import path from 'path';
// import * as dotenv from "dotenv";
import { CosmosClient } from "@azure/cosmos";
import { Parser } from '@json2csv/plainjs';

// Carga las variables de entorno desde .env
// dotenv.config();

// Configura la conexión a Cosmos DB
const cosmosClient = new CosmosClient({
    endpoint: process.env.COSMOSDB_URI,
    key: process.env.COSMOSDB_KEY,
});

const databaseId = process.env.COSMOS_DATABASE_ID;
const containerId = process.env.COSMOS_CONTAINER_ID;

// Lee el JSON desde stdin (usado por Python)
async function leerEntradaStdin() {
    return new Promise((resolve, reject) => {
        let entrada = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', chunk => entrada += chunk);
        process.stdin.on('end', () => {
            try {
                resolve(JSON.parse(entrada));
            } catch (err) {
                reject(new Error("Entrada JSON inválida"));
            }
        });
        process.stdin.on('error', err => reject(err));
    });
}

async function runQueryDinamico() {
    try {
        const input = await leerEntradaStdin();

        const database = cosmosClient.database(databaseId);
        const container = database.container(containerId);

        const query = input.query;
        const parametersObject = input.parameters || {};

        const parameters = Object.entries(parametersObject).map(([key, value]) => ({
            name: key.startsWith("@") ? key : `@${key}`,
            value: value
        }));

        const { resources } = await container.items.query({
            query,
            parameters
        }).fetchAll();

        const results = resources;

        if (!results.length) {
            console.log(JSON.stringify({ csvPath: null, message: "Sin resultados" }));
            return;
        }

        const parser = new Parser();
        const csv = parser.parse(results);

        const filePath = path.join('docs', 'telegramas', `export_c${Date.now()}.csv`);
        fs.writeFileSync(filePath, csv, 'utf8');

        console.log(JSON.stringify({ csv_path: filePath }));
    } catch (error) {
        console.error(JSON.stringify({ error: error.message }));
        process.exit(1);
    }
}

runQueryDinamico();
