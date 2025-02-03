import MaxWidthWrapper from "@/components/ui/max-width-wrapper";
import Link from "next/link";

export default function NotFound() {
  return (
    <MaxWidthWrapper className="h-screen flex flex-col items-center justify-center">
      <h2 className="text-4xl text-center font-bold">Not Found</h2>
      <p className="text-center tracking-widest">Kya dhoond raha hai 😏</p>
    </MaxWidthWrapper>
  );
}
