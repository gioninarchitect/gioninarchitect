import { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
    testDir: './tests',
    timeout: 30000,
    expect: {
        timeout: 5000
    },
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: 'html',
    use: {
        actionTimeout: 0,
        baseURL: 'http://localhost:3000',
        trace: 'on-first-retry',
        video: 'on-first-retry',
        screenshot: 'only-on-failure'
    },
    projects: [
        {
            name: 'chromium',
            use: {
                browserName: 'chromium',
            },
        },
        {
            name: 'firefox',
            use: {
                browserName: 'firefox',
            },
        },
        {
            name: 'webkit',
            use: {
                browserName: 'webkit',
            },
        },
    ],
    outputDir: 'test-results/',
    webServer: {
        command: 'npm run dev',
        port: 3000,
        timeout: 120000,
        reuseExistingServer: !process.env.CI,
    },
};

export default config;