import NextAuth, { DefaultSession } from "next-auth";
import { jwtDecode, JwtPayload } from "jwt-decode";
import Credentials from "next-auth/providers/credentials";
import axios from "axios";

export interface CustomJWTPayload extends JwtPayload {
  name: string;
  exp: number;
  token: string;
}

declare module "next-auth" {
  interface Session {
    user: {
      name: string;
      exp: number;
      token: string;
    } & DefaultSession["user"];
  }
}

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const EXPIRE_MINUTES = process.env.AUTH_EXPIRE_MINUTES;

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      credentials: {},
      authorize: async () => {
        const loginOptions = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          url: `${BACKEND_URL}/api/v1/auth/login`,
          data: {
            email: "test@test.com",
            password: "test",
          },
        };
        try {
          const response = await axios(loginOptions);
          const {
            data: {
              payload: { token },
            },
          } = response;
          const decodedToken = jwtDecode<CustomJWTPayload>(token);
          const user = {
            name: decodedToken.name as string,
            exp: decodedToken.exp as number,
            token: token as string,
          };
          return user;
        } catch (error) {
          console.error("Login error:", error);
          return null;
        }
      },
    }),
  ],
  session: {
    maxAge: Number(EXPIRE_MINUTES) * 60,
    strategy: "jwt",
  },
  trustHost: true,
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.user = user;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        session.user = token.user as typeof session.user;
      }
      return session;
    },
  },
});
