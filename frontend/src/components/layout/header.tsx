'use client';

import Link from 'next/link';
import { useState } from 'react';
import { Search, Menu, User, Bell, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useAuthStore } from '@/store/auth-store';
import { useUIStore } from '@/store/ui-store';
import { cn } from '@/lib/utils';

export function Header() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { toggleMobileMenu, theme, setTheme } = useUIStore();
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <header className="sticky top-0 z-40 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container-custom flex h-16 items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center space-x-2">
            <div className="gradient-animated h-10 w-10 rounded-lg" />
            <span className="gradient-text text-2xl font-bold">AniVibe</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link
              href="/explore"
              className="text-sm font-medium transition-colors hover:text-primary-500"
            >
              Explore
            </Link>
            <Link
              href="/search"
              className="text-sm font-medium transition-colors hover:text-primary-500"
            >
              Search
            </Link>
            <Link
              href="/atlas"
              className="text-sm font-medium transition-colors hover:text-primary-500"
            >
              Atlas
            </Link>
            {isAuthenticated && (
              <>
                <Link
                  href="/watchlist"
                  className="text-sm font-medium transition-colors hover:text-primary-500"
                >
                  My List
                </Link>
                <Link
                  href="/profile"
                  className="text-sm font-medium transition-colors hover:text-primary-500"
                >
                  Profile
                </Link>
              </>
            )}
          </nav>
        </div>

        {/* Search Bar */}
        <div className="hidden lg:flex flex-1 max-w-md mx-8">
          <Input
            placeholder="Search anime..."
            leftIcon={<Search className="h-4 w-4" />}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onClear={() => setSearchQuery('')}
            className="w-full"
          />
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center gap-4">
          {/* Search Icon (Mobile) */}
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={() => {}}
          >
            <Search className="h-5 w-5" />
          </Button>

          {isAuthenticated ? (
            <>
              {/* Notifications */}
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-5 w-5" />
                <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-primary-500" />
              </Button>

              {/* User Menu */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    className="relative h-10 w-10 rounded-full"
                  >
                    <Avatar>
                      <AvatarImage src={user?.avatar_url} />
                      <AvatarFallback>
                        {user?.username?.slice(0, 2).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none">
                        {user?.username}
                      </p>
                      <p className="text-xs leading-none text-muted-foreground">
                        {user?.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link href="/profile">Profile</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/watchlist">My List</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/settings">
                      <Settings className="mr-2 h-4 w-4" />
                      Settings
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={() => {
                      setTheme(theme === 'dark' ? 'light' : 'dark');
                    }}
                  >
                    Toggle Theme
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => logout()}>
                    Log out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Button variant="ghost" asChild>
                <Link href="/login">Login</Link>
              </Button>
              <Button variant="primary" asChild>
                <Link href="/signup">Sign Up</Link>
              </Button>
            </div>
          )}

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={toggleMobileMenu}
          >
            <Menu className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}
