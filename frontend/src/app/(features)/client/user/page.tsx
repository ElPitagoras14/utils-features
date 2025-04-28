"use client";

import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import { getProducts } from "../utils";
import { Button } from "@/components/ui/button";

export default function ClientUserPage() {
  const { data: session, status } = useSession();

  const [data, setData] = useState<any>(null);

  const getData = async () => {
    const response = await getProducts(session!.user.token);
    setData(response);
  }

  useEffect(() => {
    if (!session || data) return;
    (async () => {
      await getData();
    })();
  }, [session]);

  if (status === "loading") {
    return (
      <main className="flex flex-col justify-between">
        <div className="flex flex-col items-center justify-center min-h-screen p-24">
          <h1 className="text-2xl">Loading...</h1>
        </div>
      </main>
    );
  }

  if (status === "unauthenticated") {
    return (
      <main className="flex flex-col justify-between">
        <div className="flex flex-col items-center justify-center min-h-screen p-24">
          <h1 className="text-2xl">You are not authenticated.</h1>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col justify-between">
      <div className="flex flex-col items-center justify-center min-h-screen p-24">
        <h1 className="text-2xl">Client User Page</h1>
        <Button onClick={getData}>Refresh Data</Button>
        <p>Status: {status}</p>
        <p>Session Data: {JSON.stringify(session)}</p>
        <p>Data: {JSON.stringify(data)}</p>
      </div>
    </main>
  );
}
