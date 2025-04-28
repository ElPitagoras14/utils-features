"use client";

import { Button } from "@/components/ui/button";
import { signIn } from "next-auth/react";

export default function Login() {
  return (
    <main className="flex flex-col justify-between">
      <div className="flex flex-col items-center justify-center min-h-screen p-24">
        <Button onClick={() => signIn("credentials", { redirectTo: "/" })}>
          Login
        </Button>
      </div>
    </main>
  );
}
