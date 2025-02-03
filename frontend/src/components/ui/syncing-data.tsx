"use client";
import { motion } from "motion/react";
import MaxWidthWrapper from "./max-width-wrapper";
import { useState } from "react";
import { CheckIcon, Loader2Icon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "./button";
const STEPS = [
  { label: "Getting your data", finished: false },
  { label: "Processing", finished: false },
  { label: "Syncing", finished: false },
  { label: "Done", finished: false },
];
export default function SyncingData() {
  const [steps, setSteps] = useState(STEPS);
  const [currentStep, setCurrentStep] = useState(0);
  return (
    <MaxWidthWrapper className="flex flex-col w-full h-full justify-center items-center">
      <div>
        {steps.map((s, idx) => (
          <Step
            currentStep={currentStep === idx}
            finished={s.finished}
            label={s.label}
          />
        ))}
      </div>
      <Button
        disabled={currentStep === STEPS.length}
        onClick={() => {
          setSteps((prev) => {
            const newSteps = [...prev];
            newSteps[currentStep].finished = true;
            return newSteps;
          });
          setCurrentStep((prev) => prev + 1);
        }}
      >
        +1
      </Button>
    </MaxWidthWrapper>
  );
}

interface StepProps {
  label: string;
  finished: boolean;
  currentStep: boolean;
}
function Step({ label, finished, currentStep }: StepProps) {
  return (
    <motion.div className="flex items-center">
      {currentStep && <Loader2Icon className="size-2 shrink-0 animate-spin" />}
      {finished && <CheckIcon className="size-2 shrink-0 text-green-500" />}
      <motion.span
        className={cn("ml-2", {
          "text-neutral-500": !currentStep && !finished,
          "text-black": currentStep,
          "text-green-500": finished,
        })}
      >
        {label}
      </motion.span>
    </motion.div>
  );
}
