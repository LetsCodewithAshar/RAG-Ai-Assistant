"use client";

import { useState } from "react";
import axios from "axios";
import { Upload, Send, FileVideo, MessageSquare, Loader2 } from "lucide-react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [ingesting, setIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState("");
  
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<{role: 'user' | 'assistant', content: any}[]>([]);
  const [searching, setSearching] = useState(false);

  const handleIngest = async () => {
    if (!url) return;
    setIngesting(true);
    setIngestStatus("Downloading & Transcribing... (This may take a while)");
    try {
      const res = await axios.post("http://localhost:8000/ingest", { url });
      setIngestStatus(`Success! Processed video ID: ${res.data.video_id} with ${res.data.chunks_count} chunks.`);
    } catch (e) {
      setIngestStatus("Error ingesting video.");
      console.error(e);
    } finally {
      setIngesting(false);
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    setSearching(true);
    // Add user message
    const newMessages = [...messages, { role: 'user', content: query }];
    setMessages(newMessages); // Optimistic update
    
    try {
      const res = await axios.post("http://localhost:8000/query", { query });
      // The backend returns { results: { ids: [], distances: [], documents: [], metadatas: [] } }
      // We need to parse this.
      const docs = res.data.results.documents[0];
      const metas = res.data.results.metadatas[0];
      
      const assistantResponse = docs.map((doc: string, i: number) => ({
        text: doc,
        meta: metas[i]
      }));

      setMessages([...newMessages, { role: 'assistant', content: assistantResponse }]);
      setQuery("");
    } catch (e) {
        setMessages([...newMessages, { role: 'assistant', content: "Error fetching results." }]);
    } finally {
      setSearching(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-8 bg-slate-950 text-slate-200">
      <div className="w-full max-w-4xl space-y-8">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 text-transparent bg-clip-text">
            RAG AI Assistant
          </h1>
          <p className="text-slate-400">Chat with your videos instantly</p>
        </div>

        {/* Ingestion Section */}
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-lg">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Upload className="w-5 h-5 text-blue-400" />
            Ingest Video
          </h2>
          <div className="flex gap-4">
            <input 
              type="text" 
              placeholder="Paste YouTube URL here..." 
              className="flex-1 bg-slate-800 border-none rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button 
              onClick={handleIngest}
              disabled={ingesting}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {ingesting ? <Loader2 className="animate-spin w-4 h-4"/> : <FileVideo className="w-4 h-4"/>}
              Process
            </button>
          </div>
          {ingestStatus && (
            <div className="mt-4 p-3 bg-slate-800/50 rounded-lg text-sm text-slate-300">
              {ingestStatus}
            </div>
          )}
        </div>

        {/* Chat Section */}
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-lg min-h-[500px] flex flex-col">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-emerald-400" />
            Chat
          </h2>
          
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2 custom-scrollbar">
            {messages.length === 0 && (
              <div className="text-center text-slate-500 mt-20">
                Ask a question to search through your processed videos.
              </div>
            )}
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-2xl p-4 ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-slate-800 text-slate-200 border border-slate-700'
                }`}>
                  {msg.role === 'user' ? (
                    <p>{msg.content}</p>
                  ) : (
                     <div className="space-y-4">
                       {Array.isArray(msg.content) ? msg.content.map((item: any, i: number) => (
                         <div key={i} className="border-b border-slate-700 last:border-0 pb-2 last:pb-0">
                           <p className="mb-1">{item.text}</p>
                           <div className="text-xs text-emerald-400 font-mono">
                             [{item.meta.start.toFixed(0)}s - {item.meta.end.toFixed(0)}s] {item.meta.title}
                           </div>
                         </div>
                       )) : (
                           <p>{msg.content}</p>
                       )}
                     </div>
                  )}
                </div>
              </div>
            ))}
             {searching && (
              <div className="flex justify-start">
                 <div className="bg-slate-800 rounded-2xl p-4 border border-slate-700">
                    <Loader2 className="animate-spin w-5 h-5 text-slate-400" />
                 </div>
              </div>
            )}
          </div>

          <div className="flex gap-4 mt-auto">
            <input 
              type="text" 
              placeholder="Ask a question..." 
              className="flex-1 bg-slate-800 border-none rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-emerald-500 outline-none"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button 
              onClick={handleSearch}
              disabled={searching}
              className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>

      </div>
    </main>
  );
}
