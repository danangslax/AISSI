"use client";

import { useState } from "react";

import { createClient } from "@/lib/supabase-browser";

const supabase = createClient();

export default function LoginPage() {

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleLogin() {

    try {

      setLoading(true);

      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {

        alert(error.message);

        return;
      }

      window.location.href = "/";

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);
    }
  }

  return (

    <main className="
      min-h-screen
      bg-black
      text-white
      flex
      items-center
      justify-center
      p-8
    ">

      <div className="
        w-full
        max-w-md
        bg-zinc-900
        border
        border-zinc-800
        rounded-2xl
        p-8
      ">

        <h1 className="
          text-3xl
          font-bold
          mb-8
        ">
          AISSI Login
        </h1>

        <div className="space-y-4">

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className="
              w-full
              bg-zinc-800
              border
              border-zinc-700
              rounded-lg
              p-3
            "
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            className="
              w-full
              bg-zinc-800
              border
              border-zinc-700
              rounded-lg
              p-3
            "
          />

          <button
            onClick={handleLogin}
            disabled={loading}
            className="
              w-full
              bg-emerald-500
              text-black
              font-bold
              py-3
              rounded-lg
            "
          >

            {loading
              ? "Loading..."
              : "Login"}

          </button>

        </div>

      </div>

    </main>
  );
}