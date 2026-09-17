{
  "name": "__APP_NAME__",
  "private": true,
  "author": "",
  "scripts": {
    "build": "max build",
    "dev": "max dev",
    "format": "prettier --cache --write .",
    "postinstall": "max setup",
    "prepare": "husky",
    "setup": "max setup",
    "start": "npm run dev"
  },
  "dependencies": {
    "@ant-design/icons": "^6.3.2",
    "@ant-design/pro-components": "^3.1.14-0",
    "@umijs/max": "^4.7.8",
    "antd": "^6.6.1"
  },
  "devDependencies": {
    "@types/react": "^18.0.33",
    "@types/react-dom": "^18.0.11",
    "husky": "^9",
    "lint-staged": "^13.2.0",
    "prettier": "^2.8.7",
    "prettier-plugin-organize-imports": "^3.2.2",
    "prettier-plugin-packagejson": "^2.4.3",
    "tailwindcss": "^3.4.17",
    "typescript": "^5.0.3"
  }
}
