'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useAuthStore } from '@/store/auth-store';
import { useUIStore } from '@/store/ui-store';
import { GlitchText } from '@/components/ui/glitch-text';

export default function SettingsPage() {
  const { user } = useAuthStore();
  const { theme, setTheme } = useUIStore();
  const [username, setUsername] = useState(user?.username || '');
  const [email, setEmail] = useState(user?.email || '');

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground">Please log in to access settings</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <div className="container-custom py-12">
        <div className="mb-10">
          <GlitchText text="SYSTEM CONFIG" as="h1" className="text-4xl font-bold mb-2" />
          <p className="text-muted-foreground">Customize your interface parameters</p>
        </div>

        <Tabs defaultValue="profile">
          <TabsList className="mb-6 bg-black/40 border border-white/10 p-1 rounded-xl">
            <TabsTrigger value="profile" className="rounded-lg data-[state=active]:bg-primary-500 data-[state=active]:text-white">Profile</TabsTrigger>
            <TabsTrigger value="appearance" className="rounded-lg data-[state=active]:bg-primary-500 data-[state=active]:text-white">Appearance</TabsTrigger>
            <TabsTrigger value="notifications" className="rounded-lg data-[state=active]:bg-primary-500 data-[state=active]:text-white">Notifications</TabsTrigger>
            <TabsTrigger value="privacy" className="rounded-lg data-[state=active]:bg-primary-500 data-[state=active]:text-white">Privacy</TabsTrigger>
          </TabsList>

          <TabsContent value="profile" className="mt-6">
            <Card variant="holo">
              <CardHeader>
                <CardTitle>Profile Settings</CardTitle>
                <CardDescription>Manage your profile information</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center gap-6">
                  <Avatar className="h-24 w-24 border-2 border-primary-500/50 shadow-glow">
                    <AvatarImage src={user.avatar_url} />
                    <AvatarFallback className="text-3xl bg-primary-900 text-white">
                      {username.slice(0, 2).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  <Button variant="outline" className="border-primary-500/30 hover:border-primary-500 text-primary-300">Change Avatar</Button>
                </div>
                <Input label="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <Button variant="spirit">Save Changes</Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="appearance" className="mt-6">
            <Card variant="holo">
              <CardHeader>
                <CardTitle>Appearance</CardTitle>
                <CardDescription>Customize how AniVibe looks</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                  <div>
                    <div className="font-bold text-white mb-1">Theme</div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">
                      Current: {theme}
                    </div>
                  </div>
                  <Button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} variant="ghost">
                    Toggle Theme
                  </Button>
                </div>
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                  <div>
                    <div className="font-bold text-white mb-1">Animations</div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">
                      Enable smooth transitions
                    </div>
                  </div>
                  <Switch defaultChecked />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications" className="mt-6">
            <Card variant="holo">
              <CardHeader>
                <CardTitle>Notifications</CardTitle>
                <CardDescription>Control notification preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                  <div>
                    <div className="font-bold text-white mb-1">Email Notifications</div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">Receive updates via email</div>
                  </div>
                  <Switch defaultChecked />
                </div>
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                  <div>
                    <div className="font-bold text-white mb-1">Weekly Digest</div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">Get weekly anime summaries</div>
                  </div>
                  <Switch />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="privacy" className="mt-6">
            <Card variant="holo">
              <CardHeader>
                <CardTitle>Privacy</CardTitle>
                <CardDescription>Manage your privacy settings</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                  <div>
                    <div className="font-bold text-white mb-1">Public Profile</div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">Make profile visible to everyone</div>
                  </div>
                  <Switch defaultChecked />
                </div>
                <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                  <div>
                    <div className="font-bold text-white mb-1">Show Watchlist</div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider">Let others see your list</div>
                  </div>
                  <Switch defaultChecked />
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
