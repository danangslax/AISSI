"use client";

import { useEffect, useState } from "react";

import { createClient } from "@/lib/supabase-browser";

const supabase = createClient();

export function useAuth() {

  const [user, setUser] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    async function getSession() {

      const {
        data: { session },
      } = await supabase.auth.getSession();

      setUser(session?.user || null);

      setLoading(false);
    }

    getSession();

  }, []);

  return {
    user,
    loading,
  };
}