{
  "name": "__APP_NAME__",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build --mode standalone && node scripts/verify-build-base.mjs",
    "build:qiankun": "tsc -b && vite build --mode qiankun && node scripts/verify-build-base.mjs --require-absolute",
    "typecheck": "tsc -b --pretty false",
    "test": "vitest run"
  },
  "dependencies": {
    "@ant-design/icons": "^6.0.0",
    "antd": "^6.0.0",
    "qiankun": "^2.10.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^5.0.0",
    "typescript": "^7.0.0",
    "vite": "^8.0.0",
    "vite-plugin-qiankun": "^1.0.15",
    "vitest": "^4.0.0"
  }
}
