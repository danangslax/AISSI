interface Props {
  regime: string;
}

export default function RegimeBadge({
  regime,
}: Props) {

  const colors: Record<string, string> = {
    bullish: "bg-emerald-500",
    cautious_bullish: "bg-green-400",
    sideways: "bg-yellow-500",
    bearish: "bg-rose-500",
    panic: "bg-red-700",
  };

  return (
    <span
      className={`
        px-4 py-2 rounded-full text-sm font-semibold text-black
        ${colors[regime] || "bg-zinc-500"}
      `}
    >
      {regime}
    </span>
  );
}
