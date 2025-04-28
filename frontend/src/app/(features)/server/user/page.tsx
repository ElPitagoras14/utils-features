import { auth } from "@/auth";

export default async function ServerUserPage() {
  const session = await auth()

  return (
    <main className="flex flex-col justify-between">
      <div className="flex flex-col items-center justify-center min-h-screen p-24">
        <h1 className="text-2xl">Server User Page</h1>
        <p>{JSON.stringify(session)}</p>
      </div>
    </main>
  );
}