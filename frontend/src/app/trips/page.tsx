"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { 
  MapPin, 
  Users, 
  Calendar as CalendarIcon, 
  Star, 
  Filter,
  Search,
  SlidersHorizontal
} from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";

interface Trip {
  id: string;
  name: string;
  destinations: string[];
  startDate: string;
  endDate: string;
  price: number;
  participants: number;
  maxParticipants: number;
  organizerRating: number;
  organizerName: string;
  regions: string[];
  activities: number;
}

export default function TripsPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [startDate, setStartDate] = useState<Date>();
  const [endDate, setEndDate] = useState<Date>();
  const [selectedRegion, setSelectedRegion] = useState<string>();
  const [minBudget, setMinBudget] = useState("");
  const [maxBudget, setMaxBudget] = useState("");
  const [minRating, setMinRating] = useState<string>();

  // Mock data for trips
  const allTrips: Trip[] = [
    {
      id: "1",
      name: "Mediterranean Adventure",
      destinations: ["Barcelona", "Rome", "Athens"],
      startDate: "2025-07-15",
      endDate: "2025-07-25",
      price: 1299,
      participants: 8,
      maxParticipants: 12,
      organizerRating: 4.8,
      organizerName: "Sarah Johnson",
      regions: ["Spain", "Italy", "Greece"],
      activities: 15
    },
    {
      id: "2",
      name: "Alpine Explorer",
      destinations: ["Zurich", "Interlaken", "Zermatt"],
      startDate: "2025-08-10",
      endDate: "2025-08-18",
      price: 1850,
      participants: 6,
      maxParticipants: 10,
      organizerRating: 4.9,
      organizerName: "Marco Weber",
      regions: ["Switzerland"],
      activities: 12
    },
    {
      id: "3",
      name: "Northern Lights Quest",
      destinations: ["Reykjavik", "Akureyri"],
      startDate: "2025-09-01",
      endDate: "2025-09-08",
      price: 2100,
      participants: 4,
      maxParticipants: 8,
      organizerRating: 5.0,
      organizerName: "Erik Bjornsson",
      regions: ["Iceland"],
      activities: 8
    },
    {
      id: "4",
      name: "Bavarian Culture Tour",
      destinations: ["Munich", "Rothenburg", "Neuschwanstein"],
      startDate: "2025-07-20",
      endDate: "2025-07-27",
      price: 980,
      participants: 10,
      maxParticipants: 16,
      organizerRating: 4.6,
      organizerName: "Hans Mueller",
      regions: ["Germany"],
      activities: 10
    },
    {
      id: "5",
      name: "Portuguese Coastal Adventure",
      destinations: ["Lisbon", "Porto", "Lagos"],
      startDate: "2025-08-05",
      endDate: "2025-08-14",
      price: 1150,
      participants: 7,
      maxParticipants: 12,
      organizerRating: 4.7,
      organizerName: "Ana Silva",
      regions: ["Portugal"],
      activities: 14
    },
    {
      id: "6",
      name: "Scandinavian Explorer",
      destinations: ["Copenhagen", "Stockholm", "Oslo"],
      startDate: "2025-09-10",
      endDate: "2025-09-20",
      price: 2200,
      participants: 5,
      maxParticipants: 14,
      organizerRating: 4.8,
      organizerName: "Lars Andersen",
      regions: ["Denmark", "Sweden", "Norway"],
      activities: 18
    }
  ];

  const regions = [...new Set(allTrips.flatMap(trip => trip.regions))].sort();

  // Filter trips based on search criteria
  const filteredTrips = allTrips.filter(trip => {
    const matchesSearch = !searchTerm || 
      trip.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      trip.destinations.some(dest => dest.toLowerCase().includes(searchTerm.toLowerCase())) ||
      trip.regions.some(region => region.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesRegion = !selectedRegion || trip.regions.includes(selectedRegion);
    
    const matchesBudget = (!minBudget || trip.price >= parseInt(minBudget)) &&
                         (!maxBudget || trip.price <= parseInt(maxBudget));
    
    const matchesRating = !minRating || trip.organizerRating >= parseFloat(minRating);
    
    // Date filtering logic would go here - for now we'll skip complex date filtering
    
    return matchesSearch && matchesRegion && matchesBudget && matchesRating;
  });

  const clearFilters = () => {
    setSearchTerm("");
    setStartDate(undefined);
    setEndDate(undefined);
    setSelectedRegion(undefined);
    setMinBudget("");
    setMaxBudget("");
    setMinRating(undefined);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Discover Amazing Trips</h1>
        <p className="text-xl text-muted-foreground">
          Find the perfect travel experience organized by our community
        </p>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="space-y-6">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by destination, trip name, or region..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Filters */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Date Range */}
            <div className="space-y-2">
              <Label>Start Date</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    className={cn(
                      "w-full justify-start text-left font-normal",
                      !startDate && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {startDate ? format(startDate, "PPP") : "Pick a date"}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={startDate}
                    onSelect={setStartDate}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>

            <div className="space-y-2">
              <Label>End Date</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    className={cn(
                      "w-full justify-start text-left font-normal",
                      !endDate && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {endDate ? format(endDate, "PPP") : "Pick a date"}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={endDate}
                    onSelect={setEndDate}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>

            {/* Region Filter */}
            <div className="space-y-2">
              <Label>Region</Label>
              <Select value={selectedRegion} onValueChange={setSelectedRegion}>
                <SelectTrigger>
                  <SelectValue placeholder="Select region" />
                </SelectTrigger>
                <SelectContent>
                  {regions.map(region => (
                    <SelectItem key={region} value={region}>
                      {region}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Min Rating Filter */}
            <div className="space-y-2">
              <Label>Minimum Organizer Rating</Label>
              <Select value={minRating} onValueChange={setMinRating}>
                <SelectTrigger>
                  <SelectValue placeholder="Any rating" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="4.0">4.0+ Stars</SelectItem>
                  <SelectItem value="4.5">4.5+ Stars</SelectItem>
                  <SelectItem value="4.8">4.8+ Stars</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Budget Range */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Min Budget ($)</Label>
              <Input
                type="number"
                placeholder="0"
                value={minBudget}
                onChange={(e) => setMinBudget(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label>Max Budget ($)</Label>
              <Input
                type="number"
                placeholder="5000"
                value={maxBudget}
                onChange={(e) => setMaxBudget(e.target.value)}
              />
            </div>
          </div>

          {/* Clear Filters */}
          <div className="flex justify-between items-center">
            <p className="text-sm text-muted-foreground">
              {filteredTrips.length} trip{filteredTrips.length !== 1 ? 's' : ''} found
            </p>
            <Button variant="outline" onClick={clearFilters} size="sm">
              <SlidersHorizontal className="mr-2 h-4 w-4" />
              Clear Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Trip Results */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTrips.map((trip) => (
          <Card key={trip.id} className="overflow-hidden hover:shadow-lg transition-shadow">
            <div className="h-48 bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">
              <MapPin className="h-16 w-16 text-primary/40" />
            </div>
            <CardHeader>
              <div className="flex justify-between items-start mb-2">
                <CardTitle className="text-xl">{trip.name}</CardTitle>
                <Badge variant="secondary" className="flex items-center gap-1">
                  <Star className="h-3 w-3 fill-current" />
                  {trip.organizerRating}
                </Badge>
              </div>
              <CardDescription className="space-y-1">
                <div className="flex items-center gap-1 text-sm">
                  <MapPin className="h-4 w-4" />
                  {trip.destinations.join(" → ")}
                </div>
                <div className="text-xs text-muted-foreground">
                  by {trip.organizerName} • {trip.activities} activities
                </div>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between text-sm">
                <div className="flex items-center gap-1">
                  <CalendarIcon className="h-4 w-4" />
                  {new Date(trip.startDate).toLocaleDateString()}
                </div>
                <div className="flex items-center gap-1">
                  <Users className="h-4 w-4" />
                  {trip.participants}/{trip.maxParticipants}
                </div>
              </div>
              <div className="flex items-center gap-2 text-xs">
                {trip.regions.map(region => (
                  <Badge key={region} variant="outline" className="text-xs">
                    {region}
                  </Badge>
                ))}
              </div>
              <div className="flex justify-between items-center">
                <div className="text-2xl font-bold text-primary">
                  ${trip.price}
                </div>
                <Button asChild>
                  <Link href={`/trips/${trip.id}`}>
                    View Details
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* No Results */}
      {filteredTrips.length === 0 && (
        <Card className="p-12 text-center">
          <div className="space-y-4">
            <Search className="h-16 w-16 mx-auto text-muted-foreground" />
            <div>
              <h3 className="text-xl font-semibold mb-2">No trips found</h3>
              <p className="text-muted-foreground">
                Try adjusting your search criteria or explore all available trips
              </p>
            </div>
            <Button onClick={clearFilters} variant="outline">
              Clear All Filters
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
