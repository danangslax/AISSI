import { createClient } from "@/lib/supabase-browser";

const supabase = createClient();

export async function getPortfolio() {

  const {
    data,
    error,
  } = await supabase
    .from("portfolios")
    .select("*");

  if (error) {

    console.error(error);

    return [];
  }

  return data;
}

export async function addPortfolioPosition(
  payload: {
    symbol: string;
    quantity: number;
    average_price: number;
    user_id: string;
  }
) {

  const { error } = await supabase
    .from("portfolios")
    .insert(payload);

  if (error) {

    console.error(error);
  }
}