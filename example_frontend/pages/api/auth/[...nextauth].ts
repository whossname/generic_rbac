import NextAuth from 'next-auth'
import AzureADProvider from 'next-auth/providers/azure-ad'

export const authOptions = {
  // Configure one or more authentication providers
  providers: [
    AzureADProvider({
      clientId: process.env.AZURE_AD_CLIENT_ID ?? '',
      clientSecret: process.env.AZURE_AD_CLIENT_SECRET ?? '',
      tenantId: process.env.AZURE_AD_TENANT_ID
    })
  ],
  callbacks: {
    jwt ({ token }) {
      token.user_id = token.sub
      console.dir(token)

      // if (account) {
      //   token.accessToken = account.access_token
      //   token.id = user?.id
      // }
      return token
    }
  }
}

export default NextAuth(authOptions)
