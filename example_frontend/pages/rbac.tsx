import { ReactElement } from 'react'

export async function getStaticProps (): Promise<Object> {
  return {
    props: {
      pageId: 'rbac',
      roles: []
    }
  }
}

interface Role {
  role_name: string
  users: string[]
  permissions: string[]
  isEditable: Boolean
  isDeletable: Boolean
}

export default function RBAC (): ReactElement {
  const roles: Role[] = [
    {
      role_name: 'IT',
      users: ['Ben', 'Brad', 'Steve'],
      permissions: ['rbac'],
      isEditable: true,
      isDeletable: true
    }
  ]

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

function optionalRow (show: Boolean, body: JSX.Element): ReactElement {
  if (show) {
    return <td className='btn-cel'>{body}</td>
  } else {
    return <td />
  }
}

function roleRow (role: Role): ReactElement {
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
    <tr key={role.role_name}>
      {optionalRow(role.isDeletable, deleteCross)}
      <td>{role.role_name}</td>
      <td> <span className={isEditableClass}>{role.users.join(' - ')} </span> </td>
      <td> <span className={isEditableClass}>{role.permissions.join(' - ')} </span> </td>
    </tr>
  )
}
