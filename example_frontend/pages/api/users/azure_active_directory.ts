
async function fetchAADUsers () {
  if (!process.env.AZURE_MEMBERS_GROUP_ID) {
    throw new Error('AZURE_MEMBERS_GROUP_ID not defined')
  }


  // '/api/auth/session'
  const groupId = process.env.AZURE_MEMBERS_GROUP_ID
  const url = `https://graph.microsoft.com/v1.0/groups/${groupId}/members?$select=displayName,id`
  const res = await fetch(url)
}