import Head from 'next/head'
import { ReactElement } from 'react'

interface NavItemProps {
  title: string
  url: string
  isSelected: boolean
}

function NavItem (props: NavItemProps): ReactElement {
  const { title, url, isSelected } = props
  return (
    <li>
      <a
        className={`block px-3 py-2 transition hover:text-blue-500 ${isSelected ? 'text-blue-500' : ''}`} href={url}
        key={title}
      >{title}
      </a>
    </li>
  )
}

interface NavbarProps {
  pageId: string
}

const rbacUrl = '/rbac'

function Navbar (props: NavbarProps): ReactElement {
  return (
    <div className='mx-auto 7xl pt-6'>
      <nav>
        <ul className='flex px-3 text-slate-800 shadow-lg shadow-slate-800/5 ring-1 ring-slate-900/5 backdrop-blur'>
          <NavItem title='RBAC' url={rbacUrl} isSelected={props.pageId === 'rbac'} />
        </ul>
      </nav>
    </div>
  )
}

interface FooterLinkProps {
  text: string
  url: string
}

function FooterLink (props: FooterLinkProps): ReactElement {
  const { url, text } = props
  return <a className='transition hover:text-blue-500' href={url}>{text}</a>
}

function Footer (): ReactElement {
  return (
    <footer className='p-4 border-t flex'>
      <FooterLink text='RBAC' url={rbacUrl} />
      <p className='text-sm text-slate-400 pl-8'>© 2024 Tyson Buzza. All rights reserved.</p>
    </footer>
  )
}

export default function Layout ({ children }: any): ReactElement {
  return (
    <>
      <Head>
        <link rel='icon' href='/favicon.ico' />
        <title>RBAC</title>
      </Head>
      <div className='flex flex-col h-screen justify-between'>
        <Navbar pageId={children.props.pageId} />
        <main className='mb-auto'>{children}</main>
        <Footer />
      </div>
    </>
  )
}
