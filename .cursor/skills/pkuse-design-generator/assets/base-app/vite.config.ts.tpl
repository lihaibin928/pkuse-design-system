import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";
import qiankun from "vite-plugin-qiankun";

function requirePublicBase(value?: string): string {
  const candidate = value?.trim();
  const message =
    "qiankun build requires VITE_PUBLIC_BASE to be an absolute HTTP(S) URL";
  if (!candidate) throw new Error(message);
  let url: URL;
  try {
    url = new URL(candidate);
  } catch {
    throw new Error(message);
  }
  if (url.protocol !== "https:" && url.protocol !== "http:") {
    throw new Error(message);
  }
  return url.href.endsWith("/") ? url.href : `${url.href}/`;
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");
  const publicBase =
    mode === "qiankun" ? requirePublicBase(env.VITE_PUBLIC_BASE) : "./";

  return {
    base: publicBase,
    plugins: [react(), qiankun("__APP_NAME__", { useDevMode: true })],
    server: {
      cors: true,
      headers: { "Access-Control-Allow-Origin": "*" },
    },
  };
});
