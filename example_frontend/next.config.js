/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects () {
    return [
      {
        source: '/',
        destination: '/rbac',
        permanent: true
      }
    ]
  }
}

module.exports = nextConfig
