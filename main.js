const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 900,
        minHeight: 600,
        webPreferences: {
            // Allows your web code (app.js, etc.) to use Node.js features,
            // which is often necessary for web apps migrated to Electron.
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    // Load the existing index.html file
    // The path is relative to the root of the project (where main.js is located)
    mainWindow.loadFile('index.html');

    // Optional: Open DevTools for debugging during development
    // mainWindow.webContents.openDevTools();
}

// When Electron has finished initialization, create the window
app.whenReady().then(() => {
    createWindow();

    // Handle macOS specific behavior (re-create window when icon is clicked)
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// Quit when all windows are closed (standard Windows/Linux behavior)
app.on('window-all-closed', () => {
    // Check if the current platform is NOT macOS ('darwin')
    if (process.platform !== 'darwin') {
        app.quit();
    }
});