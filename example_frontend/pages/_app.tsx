import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import Layout from '../components/layout'
import { SessionProvider } from 'next-auth/react'
import { ReactElement } from 'react'

export default function App ({ Component, pageProps: { session, ...pageProps } }: AppProps): ReactElement {
  return (
    <SessionProvider session={session}>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </SessionProvider>
  )
}
