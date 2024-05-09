import { ReactElement } from 'react'
import useSWR from 'swr'

export interface SimplifiedRole {
  name: string
  users: string[]
  permissions: string[]
  isEditable: boolean
}

export interface ResponseError {
  message: string
}

export async function getStaticProps (): Promise<Object> {
  return {
    props: {
      pageId: 'rbac'
    }
  }
}

const fetcher = async (url: string): Promise<any> => {
  const res = await fetch(url)
  const data = await res.json()

  if (res.status !== 200) {
    throw new Error(data.message)
  }
  return data
}

export default function RBAC (): ReactElement {
  const { data, error, isLoading } =
    useSWR<SimplifiedRole[], ResponseError>(() => ('/api/rbac/fetch_all'), fetcher)

  if (error !== undefined) return <div>{error.message}</div>
  if (isLoading === true) return <div>Loading...</div>
  if (data === undefined) return <div>Missing data</div>

  const roles = data

  return (
    <section>
      <h1>RBAC</h1>

      {/* Role permissions table */}
      <section>
        <h2>Roles</h2>

        {/* Add Role */}
        <div className='m-2 pb-5'>
          <input placeholder='Role name' type='text' className='typeable' />
          <button className='bg-green-50 hover:bg-green-100'>Add Role</button>
        </div>

        <table className=''>
          <thead>
            <tr>
              <th className='w-10'> </th>
              <th> Role </th>
              <th> Users </th>
              <th> Permissions </th>
            </tr>
          </thead>

          <tbody>
            {
              roles.map((role) => roleRow(role))
            }
          </tbody>
        </table>

      </section>
    </section>
  )
}

function optionalRow (show: boolean, body: JSX.Element): ReactElement {
  if (show) {
    return <td className='btn-cel'>{body}</td>
  } else {
    return <td />
  }
}

function roleRow (role: SimplifiedRole): ReactElement {
  const deleteCross = (
    <span className='
    cursor-pointer w-full px-2 my-1 inline-block
    bg-red-50 hover:bg-red-200
    text-center text-red-600 text-xl font-black
    '
    > <text> &times; </text>
    </span>
  )

  const isEditableClass = role.isEditable
    ? 'cursor-pointer w-full px-2 py-1 m-1 inline-block bg-yellow-50 hover:bg-yellow-100 '
    : ''

  return (
    <tr key={role.name}>
      {optionalRow(role.isEditable, deleteCross)}
      <td>{role.name}</td>
      <td> <span className={isEditableClass}>{role.users.join(' - ')} </span> </td>
      <td> <span className={isEditableClass}>{role.permissions.join(' - ')} </span> </td>
    </tr>
  )
}
