import { ReactNode } from "react";

interface Props {
  title: string;
  children: ReactNode;
}

export default function DashboardCard({
  title,
  children,
}: Props) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-4 text-white">
        {title}
      </h2>

      {children}
    </div>
  );
}
