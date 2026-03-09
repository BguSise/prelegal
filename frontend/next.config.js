/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  // Static export defaults to 'out' directory, which works for Docker multi-stage build
};

export default nextConfig;
