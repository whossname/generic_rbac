import type { NextApiRequest, NextApiResponse } from 'next'
import type { SimplifiedRole } from '@/pages/rbac'

interface RBACRoot {
  permissions: Permission[]
  roles: Role[]
}

interface Permission {
  id: number
  name: string
}

interface RolePermission {
  permission_id: number
  write_access: boolean
}

interface Role {
  id: number
  is_everyone: boolean
  is_super_admin: boolean
  name: string
  role_permissions: RolePermission[]
  user_ids: string[]
}

export default async function handler (_req: NextApiRequest, res: NextApiResponse): Promise<void> {
  const baseUrl = process.env.RBAC_SERVICE_BASE_URL ?? ''
  const url = baseUrl + '/rbac/fetch-all/'
  const rbacRes = await fetch(url)

  if (!rbacRes.ok) {
    // This will activate the closest `error.js` Error Boundary
    throw new Error('Failed to fetch data')
  }

  const rbac: RBACRoot = await rbacRes.json()
  const permissions: Array<[number, string]> =
    rbac.permissions.map(permission => [permission.id, permission.name])
  const permissionMap = new Map(permissions)

  const roles: SimplifiedRole[] = rbac.roles.map(role => {
    return {
      name: role.name,
      // TODO need to get users as well
      users: role.user_ids,
      permissions: role.role_permissions.map(rp => permissionMap.get(rp.permission_id) ?? ''),
      isEditable: !role.is_everyone && !role.is_super_admin
    }
  })

  res.status(200).json(roles)
}
