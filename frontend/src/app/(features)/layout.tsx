import { signOut } from "@/auth";
import { Button } from "@/components/ui/button";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import { SessionProvider } from "next-auth/react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Utils Features App",
  description: "Web for utils features",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="flex flex-col justify-between items-center text-xl py-6">
          <div className="flex space-x-4">
            <Link href={"/client/user"} className="hover:text-primary">
              Client User
            </Link>
            <Link href={"/client/product"} className="hover:text-primary">
              Client Product
            </Link>
            <Link href={"/server/user"} className="hover:text-primary">
              Server User
            </Link>
            <Link href={"/server/product"} className="hover:text-primary">
              Server Product
            </Link>
            <Button
              onClick={async () => {
                "use server";
                await signOut({
                  redirectTo: "/login",
                });
              }}
              className="hover:cursor-pointer"
            >
              Logout
            </Button>
          </div>
        </div>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
