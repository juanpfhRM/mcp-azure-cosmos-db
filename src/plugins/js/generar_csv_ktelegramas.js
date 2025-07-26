import fs from 'fs';
import path from 'path';
import { DefaultAzureCredential } from "@azure/identity";
import { LogsQueryClient } from "@azure/monitor-query";
import { Parser } from '@json2csv/plainjs';

// Leer el JSON desde stdin
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
        const resourceId = "/subscriptions/3276bda1-f68f-4013-aff1-6b2be2bfc8ef/resourceGroups/Mdlewre-eastus-nprd-app-rg-01/providers/Microsoft.OperationalInsights/workspaces/log-pruebas-1";

        const query = input.query;

        const credential = new DefaultAzureCredential();
        const logClient = new LogsQueryClient(credential);

        const result = await logClient.queryResource(resourceId, query, {
            duration: "P1D", // Último día
        });

        if (!result.tables || result.tables.length === 0 || result.tables[0].rows.length === 0) {
            console.log(JSON.stringify({ csvPath: null, message: "Sin resultados" }));
            return;
        }

        const table = result.tables[0];
        const rows = table.rows.map(row => {
            const obj = {};
            row.forEach((cell, idx) => {
                obj[table.columns[idx].name] = cell;
            });
            return obj;
        });

        const parser = new Parser();
        const csv = parser.parse(rows);

        const dirPath = path.join('docs', 'telegramas');
        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
        }

        const filePath = path.join(dirPath, `export_k${Date.now()}.csv`);
        fs.writeFileSync(filePath, csv, 'utf8');

        console.log(JSON.stringify({ csv_path: filePath }));
    } catch (error) {
        console.error(JSON.stringify({ error: error.message }));
        process.exit(0);
    }
}

runQueryDinamico();
