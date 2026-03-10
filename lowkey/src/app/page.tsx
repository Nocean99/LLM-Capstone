import { HeroSection } from "@/components/HeroSection";
import { ChannelRack } from "@/components/ChannelRack";
import { ArtistGrid } from "@/components/ArtistGrid";
import { HallOfFame } from "@/components/HallOfFame";

export default function Home() {
  return (
    <div className="min-h-full">
      <HeroSection />
      <ChannelRack />
      <ArtistGrid />
      <HallOfFame />
    </div>
  );
}
