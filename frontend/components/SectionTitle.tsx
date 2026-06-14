interface Props {
  title: string;
  subtitle?: string;
}

export default function SectionTitle({
  title,
  subtitle,
}: Props) {
  return (
    <div className="mb-8">
      <h1 className="text-4xl font-bold text-white">
        {title}
      </h1>

      {subtitle && (
        <p className="text-zinc-400 mt-2">
          {subtitle}
        </p>
      )}
    </div>
  );
}