#!/usr/bin/env node

const { EventSource } = require('eventsource');
const https = require('https');
const http = require('http');
const url = require('url');

// Configuration
const OPENMEMORY_URL = 'http://localhost:8765/mcp/claude/sse/moot';
const MESSAGE_URL = 'http://localhost:8765/mcp/claude/sse/moot/messages/';

class OpenMemoryMCPBridge {
    constructor() {
        this.eventSource = null;
        this.sessionId = null;
        this.messageQueue = [];
        this.isInitialized = false;
    }

    async initialize() {
        try {
            // Connect to the SSE endpoint
            this.eventSource = new EventSource(OPENMEMORY_URL);
            
            this.eventSource.onopen = () => {
                console.error('Connected to OpenMemory MCP server');
                this.isInitialized = true;
                this.processMessageQueue();
            };

            this.eventSource.onmessage = (event) => {
                if (event.data) {
                    try {
                        const data = JSON.parse(event.data);
                        // Forward MCP messages to Claude Desktop
                        console.log(JSON.stringify(data));
                    } catch (e) {
                        console.error('Error parsing message:', e);
                    }
                }
            };

            this.eventSource.addEventListener('endpoint', (event) => {
                // Extract session ID from the endpoint event
                const endpointData = event.data;
                if (endpointData && endpointData.includes('session_id=')) {
                    this.sessionId = endpointData.split('session_id=')[1];
                    console.error('Session ID:', this.sessionId);
                }
            });

            this.eventSource.onerror = (error) => {
                console.error('SSE connection error:', error);
                if (this.eventSource.readyState === EventSource.CLOSED) {
                    console.error('Connection closed, attempting to reconnect...');
                    setTimeout(() => this.initialize(), 5000);
                }
            };

            // Handle stdin from Claude Desktop
            process.stdin.on('data', (data) => {
                const message = data.toString().trim();
                if (message) {
                    this.sendMessage(message);
                }
            });

            // Send initial initialization
            setTimeout(() => {
                this.sendMessage(JSON.stringify({
                    jsonrpc: "2.0",
                    method: "initialize",
                    params: {
                        protocolVersion: "2024-11-05",
                        capabilities: {
                            roots: { listChanged: true },
                            sampling: {}
                        },
                        clientInfo: {
                            name: "claude-desktop",
                            version: "1.0.0"
                        }
                    },
                    id: 1
                }));
            }, 1000);

        } catch (error) {
            console.error('Failed to initialize OpenMemory MCP bridge:', error);
            process.exit(1);
        }
    }

    async sendMessage(message) {
        if (!this.isInitialized) {
            this.messageQueue.push(message);
            return;
        }

        try {
            const requestBody = message;
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(requestBody)
                }
            };

            const req = http.request(MESSAGE_URL, requestOptions, (res) => {
                let responseData = '';
                res.on('data', (chunk) => {
                    responseData += chunk;
                });
                res.on('end', () => {
                    if (responseData) {
                        try {
                            const response = JSON.parse(responseData);
                            console.log(JSON.stringify(response));
                        } catch (e) {
                            console.error('Error parsing response:', e);
                        }
                    }
                });
            });

            req.on('error', (error) => {
                console.error('Request error:', error);
            });

            req.write(requestBody);
            req.end();

        } catch (error) {
            console.error('Error sending message:', error);
        }
    }

    processMessageQueue() {
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            this.sendMessage(message);
        }
    }
}

// Handle process termination
process.on('SIGINT', () => {
    console.error('Shutting down OpenMemory MCP bridge...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.error('Shutting down OpenMemory MCP bridge...');
    process.exit(0);
});

// Start the bridge
const bridge = new OpenMemoryMCPBridge();
bridge.initialize(); 