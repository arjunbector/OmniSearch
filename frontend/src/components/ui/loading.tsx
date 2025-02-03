import { Loader2 } from "lucide-react";

export default function Loading() {
  return (
    <div className="flex justify-center items-center h-full min-h-20">
      <Loader2 className="w-10 h-10 animate-spin text-primary" />
      <h6>Loading...</h6>
    </div>
  );
}
