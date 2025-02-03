"use client";
import React, { useState, useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ExternalLink, FileText, Sheet, Loader2 } from "lucide-react";
import { format } from "date-fns";
import Loading from "@/components/ui/loading";

const API_ENDPOINT = process.env.NEXT_PUBLIC_API_ENDPOINT;

const FileTypeIcon = ({ type }: { type: string }) => {
  switch (type) {
    case "Google Sheet":
      return <Sheet className="shrink-0 w-5 h-5 text-green-600" />;
    case "PDF":
      return <FileText className="shrink-0 w-5 h-5 text-red-600" />;
    default:
      return <FileText className="shrink-0 w-5 h-5 text-blue-600" />;
  }
};

interface fileType {
  id?: string;
  name?: string;
  type?: string;
  modified?: string;
  viewLink?: string;
}

export default function FilesDashboard() {
  const [files, setFiles] = useState<fileType[]>([]);
  const [activeTab, setActiveTab] = useState("All Files");
  const [isLoading, setIsLoading] = useState(true);

  const getFiles = async () => {
    try {
      setIsLoading(true);
      const res = await fetch(`${API_ENDPOINT}/auth/drive/files`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Failed to fetch files");
      }

      const data = await res.json();
      setFiles(data.files);
    } catch (error) {
      console.error("Error fetching files:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    getFiles();
  }, []);

  // Group files by type
  const filesByType = files.reduce(
    (acc, file) => {
      // @ts-ignore
      if (!acc[file.type]) {
        // @ts-ignore
        acc[file.type] = [];
      }
      // @ts-ignore
      acc[file.type].push(file);
      return acc;
    },
    { "All Files": files }
  );

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      {files.length === 0 ? (
        <div className="text-center text-muted-foreground">No files found</div>
      ) : (
        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="space-y-4"
        >
          <TabsList className="flex justify w-full gap-2">
            {Object.keys(filesByType).map((type) => (
              <TabsTrigger key={type} value={type}>
                {/* @ts-ignore */}
                {type} ({filesByType[type].length})
              </TabsTrigger>
            ))}
          </TabsList>

          {Object.entries(filesByType).map(([type, typeFiles]) => (
            <TabsContent key={type} value={type}>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {typeFiles.map((file) => (
                  <Card key={file.id} className="w-full">
                    <CardHeader className="flex flex-row items-center space-x-4 pb-2">
                      <FileTypeIcon type={file.type as string} />
                      <CardTitle className="text-sm line-clamp-1">
                        {file.name}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm text-muted-foreground space-y-1">
                      <p>Type: {file.type}</p>
                      <p>
                        Last Modified:{" "}
                        {format(
                          new Date(file.modified as string),
                          "MMM dd, yyyy HH:mm"
                        )}
                      </p>
                    </CardContent>
                    <CardFooter className="justify-end">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => window.open(file.viewLink, "_blank")}
                      >
                        <ExternalLink className="mr-2 w-4 h-4" />
                        View
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </TabsContent>
          ))}
        </Tabs>
      )}
    </div>
  );
}
