import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { TransportBar } from "@/components/TransportBar";
import { Sidebar } from "@/components/Sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Lowkey — Discover Underground Music",
  description:
    "A streaming platform for underground artists. Once you hit 100K listeners, you graduate to the Hall of Fame.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="flex h-screen w-screen flex-col overflow-hidden">
          {/* Top Menu Bar - like FL Studio's menu */}
          <header className="flex h-8 shrink-0 items-center border-b border-fl-border bg-fl-bg-dark px-3">
            <div className="flex items-center gap-1">
              <span className="font-mono text-sm font-bold tracking-wider text-fl-orange">
                LOWKEY
              </span>
              <span className="ml-1 rounded bg-fl-orange/20 px-1.5 py-0.5 font-mono text-[10px] text-fl-orange">
                v1.0
              </span>
            </div>
            <nav className="ml-6 flex items-center gap-4">
              {["Discover", "Artists", "Genres", "Hall of Fame"].map((item) => (
                <button
                  key={item}
                  className="font-mono text-xs text-fl-text-secondary transition-colors hover:text-fl-orange"
                >
                  {item}
                </button>
              ))}
            </nav>
            <div className="ml-auto flex items-center gap-3">
              <button className="rounded border border-fl-border px-3 py-0.5 font-mono text-xs text-fl-text-secondary transition-colors hover:border-fl-orange hover:text-fl-orange">
                Sign In
              </button>
              <button className="rounded bg-fl-orange px-3 py-0.5 font-mono text-xs font-medium text-black transition-colors hover:bg-fl-orange-bright">
                Join
              </button>
            </div>
          </header>

          {/* Main Content Area */}
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-y-auto bg-fl-bg-darkest">
              {children}
            </main>
          </div>

          {/* Transport Bar - FL Studio's playback controls */}
          <TransportBar />
        </div>
      </body>
    </html>
  );
}
