import { useState } from 'react';
import { AppShell, type TabId } from './components/AppShell';
import { Dashboard } from './components/Dashboard';
import { Chat } from './components/Chat';
import { Specializations } from './components/Specializations';
import { Agents } from './components/Agents';
import { Tasks } from './components/Tasks';

function App() {
  const [activeTab, setActiveTab] = useState<TabId>('dashboard');

  return (
    <AppShell activeTab={activeTab} onNavigate={setActiveTab}>
      {({ status, liveEvent }) => (
        <>
          {activeTab === 'dashboard' && <Dashboard status={status} liveEvent={liveEvent} />}
          {activeTab === 'chat' && <Chat />}
          {activeTab === 'specializations' && <Specializations />}
          {activeTab === 'agents' && <Agents />}
          {activeTab === 'tasks' && <Tasks liveEvent={liveEvent} />}
        </>
      )}
    </AppShell>
  );
}

export default App;
