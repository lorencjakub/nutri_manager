/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'jest-environment-jsdom',
    globals: {
        "ts-jest": {
          tsconfig: "./tsconfig.jest.json",
          isolatedModules: true
        }
    },
    setupFiles: ["./src/tests/testSetup.tsx"],
    setupFilesAfterEnv: ["./jest.setup.ts"],
    transform: {
      '\\.(ts|tsx)$': 'ts-jest',
      "\\.(js|jsx)$": "./jest.babel.js",
      ".+\\.(css|scss|png|jpg|svg)$": "jest-transform-stub"
    },
    testMatch: [
      "**/*.(test|spec).(ts|tsx)"
    ],
    transformIgnorePatterns: [
      "/node_modules/(?!(uuid|@bundled-es-modules))",
    ],
    collectCoverageFrom: [
      "src/**/*.ts*"
    ],
    coverageReporters: ["text"],
    coveragePathIgnorePatterns: [
      "node_modules",
      "src/index.tsx"
  ]
}