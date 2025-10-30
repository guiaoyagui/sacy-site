import React from "react";

interface ServiceCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

export default function ServiceCard({ icon, title, description }: ServiceCardProps) {
  return (
    <div className="bg-black/40 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-black/60 hover:border-white/40 transition-all duration-300 group">
      <div className="mb-4 text-white group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-300 text-sm leading-relaxed">{description}</p>
    </div>
  );
}