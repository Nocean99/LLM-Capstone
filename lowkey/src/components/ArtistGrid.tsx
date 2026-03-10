"use client";

import { ArtistCard } from "./ArtistCard";

const artists = [
  { name: "KVNG", genre: "Hip Hop", listeners: 45200, color: "#ff6600" },
  { name: "Synthwave.exe", genre: "Electronic", listeners: 32100, color: "#4a9eff" },
  { name: "Amara Joy", genre: "R&B / Soul", listeners: 87400, color: "#ff3333" },
  { name: "lofi.sage", genre: "Lo-Fi", listeners: 28900, color: "#7ed321" },
  { name: "Brick$", genre: "Hip Hop", listeners: 93100, color: "#ffd700" },
  { name: "Echo Park", genre: "Ambient", listeners: 15600, color: "#00d4aa" },
  { name: "NullPtr", genre: "Electronic", listeners: 61200, color: "#9966ff" },
  { name: "Detroitwave", genre: "Indie", listeners: 71800, color: "#ff6699" },
];

export function ArtistGrid() {
  return (
    <div className="px-8 py-6">
      <div className="mb-4 flex items-center gap-3">
        <div className="flex items-center gap-1.5">
          <div className="h-3 w-3 rounded-sm bg-fl-green" />
          <h2 className="font-mono text-sm font-bold uppercase tracking-wider text-fl-text-primary">
            Rising Artists
          </h2>
        </div>
        <div className="h-px flex-1 bg-fl-border" />
        <span className="font-mono text-[10px] text-fl-text-muted">
          {artists.length} ARTISTS
        </span>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {artists.map((artist, i) => (
          <ArtistCard key={artist.name} {...artist} index={i} />
        ))}
      </div>
    </div>
  );
}
