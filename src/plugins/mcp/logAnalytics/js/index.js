#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import { DefaultAzureCredential } from "@azure/identity";
import { LogsQueryClient } from "@azure/monitor-query";

process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err.message || err);
});

process.on('unhandledRejection', (reason) => {
    console.error('Unhandled Rejection:', reason?.message || reason);
});

const logAnalyticsWorkspaceId = process.env.LOG_ANALYTICS_WORKSPACE_ID;

if (!logAnalyticsWorkspaceId) {
    console.error("Faltan variables de entorno necesarias.");
    process.exit(1);
}

const credential = new DefaultAzureCredential();
const logClient = new LogsQueryClient(credential);

const QUERY_LOGS_TOOL = {
    name: "query_logs",
    description: "Run a KQL query in Azure Log Analytics",
    inputSchema: {
        type: "object",
        properties: {
            query: { type: "string", description: "Query in KQL language" },
        },
        required: ["query"],
    },
};

/**
 * Formats query results into a readable table
 * @param tables The tables returned from the query
 * @returns Formatted string representation of the tables
 */
function formatResults(tables) {
    if (!tables || tables.length === 0) {
        return "No results found.";
    }

    let output = "";

    for (const table of tables) {
        if (!table.rows || table.rows.length === 0) {
            output += "Table returned no rows.\n";
            continue;
        }

        const columns = table.columns.map((col) => col.name);
        const columnWidths = columns.map((col) => col.length);

        table.rows.forEach((row) => {
            for (let i = 0; i < row.length; i++) {
                const cellValue = String(row[i] === null ? "NULL" : row[i]);
                columnWidths[i] = Math.max(columnWidths[i], cellValue.length);
            }
        });

        let headerRow = "| ";
        let separatorRow = "| ";

        for (let i = 0; i < columns.length; i++) {
            const column = columns[i];
            const width = columnWidths[i];
            headerRow += column.padEnd(width) + " | ";
            separatorRow += "-".repeat(width) + " | ";
        }

        output += headerRow + "\n";
        output += separatorRow + "\n";

        for (const row of table.rows) {
            let dataRow = "| ";
            for (let i = 0; i < row.length; i++) {
                const cellValue = String(row[i] === null ? "NULL" : row[i]);
                dataRow += cellValue.padEnd(columnWidths[i]) + " | ";
            }
            output += dataRow + "\n";
        }
        output += `\n(${table.rows.length} rows)\n\n`;
    }
    return output;
}

/**
 * Executes a KQL query against Application Insights
 * @param kqlQuery The KQL query to execute
 * @returns Promise containing the formatted results as a string
 */
async function queryLogs(kqlQuery) {
    try {
        const result = await logClient.queryWorkspace(
            logAnalyticsWorkspaceId,
            kqlQuery.toString(),
        );

        return formatResults(result.tables);
    } catch (error) {
        const safeErrorMessage = (error && typeof error === 'object' && 'message' in error)
            ? error.message
            : String(error);

        return {
            success: false,
            message: `Failed to query workspace: ${safeErrorMessage}`,
            items: [],
        };
    }
}

const server = new Server({
    name: "azure-log-analytics-mcp",
    version: "0.1.0",
}, {
    capabilities: {
        tools: {},
    },
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [QUERY_LOGS_TOOL],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
        if (request.params.name === "query_logs") {
            const { query } = request.params.arguments;
            const result = await queryLogs(query);
            return {
                content: [{ type: "text", text: result }],
                isError: !result.success,
            };
        }

        return {
            content: [{ type: "text", text: `Error: Tool not implemented: ${request.params.name}` }],
            isError: true,
        };
    } catch (err) {
        return {
            content: [{ type: "text", text: `Error: ${err.message}` }],
            isError: true,
        };
    }
});

async function runServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Azure Log Analytics MCP Server ejecutándose por stdio.");
}

runServer().catch((err) => {
    console.error("Fallo al iniciar el servidor:", err);
    process.exit(1);
});
