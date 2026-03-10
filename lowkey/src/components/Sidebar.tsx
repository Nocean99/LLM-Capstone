"use client";

import { useState } from "react";
import { motion } from "framer-motion";

const channels = [
  { name: "Hip Hop", color: "#ff6600", active: true },
  { name: "Electronic", color: "#4a9eff", active: false },
  { name: "R&B / Soul", color: "#ff3333", active: false },
  { name: "Lo-Fi", color: "#7ed321", active: false },
  { name: "Indie", color: "#ffd700", active: false },
  { name: "Jazz", color: "#00d4aa", active: false },
  { name: "Ambient", color: "#9966ff", active: false },
  { name: "Punk", color: "#ff6699", active: false },
];

export function Sidebar() {
  const [activeChannel, setActiveChannel] = useState(0);
  const [collapsed, setCollapsed] = useState(false);

  return (
    <motion.aside
      className="fl-panel-raised flex shrink-0 flex-col border-r border-fl-border bg-fl-bg-dark"
      animate={{ width: collapsed ? 48 : 200 }}
      transition={{ duration: 0.2 }}
    >
      {/* Channel Rack Header */}
      <div className="flex h-7 items-center justify-between border-b border-fl-border px-2">
        {!collapsed && (
          <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-fl-text-muted">
            Genres
          </span>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="ml-auto flex h-5 w-5 items-center justify-center rounded text-fl-text-muted transition-colors hover:text-fl-orange"
        >
          <span className="text-xs">{collapsed ? "»" : "«"}</span>
        </button>
      </div>

      {/* Channel Rack - Genre List */}
      <div className="flex-1 overflow-y-auto py-1">
        {channels.map((channel, i) => (
          <button
            key={channel.name}
            onClick={() => setActiveChannel(i)}
            className={`group flex w-full items-center gap-2 px-2 py-1.5 transition-colors ${
              activeChannel === i
                ? "bg-fl-bg-light"
                : "hover:bg-fl-bg-medium"
            }`}
          >
            {/* Channel LED indicator */}
            <div
              className="h-2.5 w-2.5 shrink-0 rounded-full transition-all"
              style={{
                backgroundColor:
                  activeChannel === i ? channel.color : "transparent",
                border: `1.5px solid ${channel.color}`,
                boxShadow:
                  activeChannel === i
                    ? `0 0 6px ${channel.color}40`
                    : "none",
              }}
            />

            {!collapsed && (
              <>
                {/* Step sequencer dots */}
                <div className="flex gap-[2px]">
                  {[0, 1, 2, 3].map((step) => (
                    <div
                      key={step}
                      className="h-1.5 w-1.5 rounded-[1px]"
                      style={{
                        backgroundColor:
                          activeChannel === i && step < 3
                            ? channel.color
                            : "var(--fl-bg-lighter)",
                      }}
                    />
                  ))}
                </div>

                <span
                  className={`font-mono text-xs transition-colors ${
                    activeChannel === i
                      ? "text-fl-text-primary"
                      : "text-fl-text-secondary group-hover:text-fl-text-primary"
                  }`}
                >
                  {channel.name}
                </span>

                {/* Fake track count */}
                <span className="ml-auto font-mono text-[10px] text-fl-text-muted">
                  {Math.floor(Math.random() * 500 + 50)}
                </span>
              </>
            )}
          </button>
        ))}
      </div>

      {/* Bottom section - Playlist/Browser toggle */}
      <div className="border-t border-fl-border p-2">
        {!collapsed && (
          <div className="flex flex-col gap-1">
            <SidebarButton icon="♫" label="My Playlist" />
            <SidebarButton icon="★" label="Hall of Fame" highlight />
            <SidebarButton icon="↑" label="Upload Track" />
          </div>
        )}
      </div>
    </motion.aside>
  );
}

function SidebarButton({
  icon,
  label,
  highlight,
}: {
  icon: string;
  label: string;
  highlight?: boolean;
}) {
  return (
    <button
      className={`flex items-center gap-2 rounded px-2 py-1.5 text-left font-mono text-xs transition-colors ${
        highlight
          ? "text-fl-yellow hover:bg-fl-yellow/10"
          : "text-fl-text-secondary hover:bg-fl-bg-medium hover:text-fl-text-primary"
      }`}
    >
      <span>{icon}</span>
      <span>{label}</span>
    </button>
  );
}
