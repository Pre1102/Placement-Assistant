import React, { useState, useRef, useEffect } from 'react';
import { BotMessageSquare, Send, Sparkles, RefreshCw } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import ChatMessage from '../components/ChatMessage';
import LoadingSpinner from '../components/LoadingSpinner';
import { askChat } from '../services/api';

const PROMPT_SUGGESTIONS = [
  "Am I eligible for Demo Company A with 1 active backlog?",
  "What is the minimum CGPA requirement for Demo Company B?",
  "What are the official rules for One Student One Job policy?",
  "What documents are required for placement registration?",
  "How should I prepare for a Data Analyst campus role?",
  "What is the policy for Semester 8 full-time internships?"
];

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      category: 'GENERAL',
      text: "Hello! I am your CareerCampusAI Placement Assistant. Ask me anything about placement rules, company criteria, backlog policies, or career guidance.",
      sources: []
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText = inputQuery) => {
    const q = queryText.trim();
    if (!q || loading) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: q
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const response = await askChat(q);
      const assistantMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        category: response.category,
        text: response.answer,
        eligibility_result: response.eligibility_result,
        sources: response.sources,
        unknown_query: response.unknown_query
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Chat API error:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'assistant',
          category: 'GENERAL',
          text: "I encountered an error connecting to the placement intelligence engine. Please check your backend connection.",
          unknown_query: true
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] max-w-5xl mx-auto">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
            <BotMessageSquare className="w-6 h-6 text-emerald-600" />
            <span>Placement & Career AI Assistant</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Source-grounded RAG query processor with automated intent classification
          </p>
        </div>
        <Button 
          variant="outline" 
          size="sm" 
          onClick={() => setMessages([messages[0]])}
        >
          <RefreshCw className="w-3.5 h-3.5 mr-1" />
          <span>Clear Chat</span>
        </Button>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-4 px-1 space-y-4">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="flex items-center space-x-2 p-4 bg-white rounded-2xl border border-slate-200 w-fit">
            <LoadingSpinner label="Retrieving grounded context & synthesizing answer..." size="sm" />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Prompt Suggestions */}
      <div className="py-2 overflow-x-auto flex items-center space-x-2 no-scrollbar">
        <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center space-x-1 flex-shrink-0">
          <Sparkles className="w-3 h-3 text-emerald-600" />
          <span>Suggested:</span>
        </span>
        {PROMPT_SUGGESTIONS.map((s, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(s)}
            className="px-3 py-1 bg-slate-100 hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 border border-slate-200 hover:border-emerald-200 rounded-full text-xs font-medium whitespace-nowrap transition-colors"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Input Box Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="mt-2 bg-white rounded-2xl border border-slate-200 p-2 flex items-center space-x-2 shadow-sm focus-within:border-emerald-500 focus-within:ring-2 focus-within:ring-emerald-500/10"
      >
        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          placeholder="Ask about placement rules, company requirements, backlogs, or career guidance..."
          className="flex-1 px-3 py-2 text-sm bg-transparent focus:outline-none text-slate-900 placeholder:text-slate-400"
        />
        <Button
          type="submit"
          disabled={!inputQuery.trim() || loading}
          className="rounded-xl shadow-xs"
        >
          <Send className="w-4 h-4" />
        </Button>
      </form>

    </div>
  );
}
