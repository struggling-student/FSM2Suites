"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  MapPin, 
  Users, 
  Calendar as CalendarIcon, 
  Star, 
  Edit,
  Trash2,
  PlusCircle,
  Settings,
  Eye
} from "lucide-react";
import { toast } from "sonner";

interface Trip {
  id: string;
  name: string;
  destinations: string[];
  startDate: string;
  endDate: string;
  price: number;
  participants: number;
  maxParticipants: number;
  status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled';
  role: 'organizer' | 'participant';
  organizerName?: string;
  organizerRating?: number;
}

export default function MyTripsPage() {
  const [trips] = useState<Trip[]>([
    {
      id: "1",
      name: "Mediterranean Adventure",
      destinations: ["Barcelona", "Rome", "Athens"],
      startDate: "2025-07-15",
      endDate: "2025-07-25",
      price: 1299,
      participants: 8,
      maxParticipants: 12,
      status: "upcoming",
      role: "organizer"
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
      status: "upcoming",
      role: "participant",
      organizerName: "Marco Weber",
      organizerRating: 4.9
    },
    {
      id: "3",
      name: "Tuscany Wine Tour",
      destinations: ["Florence", "Siena", "Montepulciano"],
      startDate: "2024-09-12",
      endDate: "2024-09-18",
      price: 890,
      participants: 10,
      maxParticipants: 10,
      status: "completed",
      role: "organizer"
    },
    {
      id: "4",
      name: "Northern Lights Quest",
      destinations: ["Reykjavik", "Akureyri"],
      startDate: "2025-02-01",
      endDate: "2025-02-08",
      price: 2100,
      participants: 4,
      maxParticipants: 8,
      status: "upcoming",
      role: "participant",
      organizerName: "Erik Bjornsson",
      organizerRating: 5.0
    },
    {
      id: "5",
      name: "Portuguese Coastal Adventure",
      destinations: ["Lisbon", "Porto", "Lagos"],
      startDate: "2024-05-20",
      endDate: "2024-05-29",
      price: 1150,
      participants: 12,
      maxParticipants: 12,
      status: "completed",
      role: "participant",
      organizerName: "Ana Silva",
      organizerRating: 4.7
    }
  ]);

  const organizedTrips = trips.filter(trip => trip.role === "organizer");
  const joinedTrips = trips.filter(trip => trip.role === "participant");

  const getStatusColor = (status: string) => {
    const colors = {
      upcoming: "bg-blue-100 text-blue-800",
      ongoing: "bg-green-100 text-green-800",
      completed: "bg-gray-100 text-gray-800",
      cancelled: "bg-red-100 text-red-800"
    };
    return colors[status as keyof typeof colors] || "bg-gray-100 text-gray-800";
  };

  const getRoleColor = (role: string) => {
    return role === "organizer" 
      ? "bg-purple-100 text-purple-800" 
      : "bg-orange-100 text-orange-800";
  };

  const handleDeleteTrip = (tripId: string) => {
    // In a real app, this would make an API call
    toast.success("Trip deleted successfully");
  };

  const TripCard = ({ trip }: { trip: Trip }) => (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow">
      <div className="h-32 bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">
        <MapPin className="h-12 w-12 text-primary/40" />
      </div>
      <CardHeader>
        <div className="flex justify-between items-start mb-2">
          <CardTitle className="text-lg">{trip.name}</CardTitle>
          <div className="flex gap-2">
            <Badge className={getStatusColor(trip.status)}>
              {trip.status}
            </Badge>
            <Badge className={getRoleColor(trip.role)}>
              {trip.role}
            </Badge>
          </div>
        </div>
        <CardDescription className="space-y-1">
          <div className="flex items-center gap-1 text-sm">
            <MapPin className="h-4 w-4" />
            {trip.destinations.join(" → ")}
          </div>
          {trip.role === "participant" && trip.organizerName && (
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              <Star className="h-3 w-3" />
              by {trip.organizerName} ({trip.organizerRating}/5)
            </div>
          )}
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
        
        <div className="flex justify-between items-center">
          <div className="text-xl font-bold text-primary">
            ${trip.price}
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" asChild>
              <Link href={`/trips/${trip.id}`}>
                <Eye className="h-4 w-4" />
              </Link>
            </Button>
            {trip.role === "organizer" && (
              <>
                <Button variant="outline" size="sm" asChild>
                  <Link href={`/trips/${trip.id}/edit`}>
                    <Edit className="h-4 w-4" />
                  </Link>
                </Button>
                {trip.status === "upcoming" && (
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => handleDeleteTrip(trip.id)}
                    className="text-destructive hover:text-destructive"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                )}
              </>
            )}
            {trip.role === "organizer" && trip.status === "upcoming" && (
              <Button variant="outline" size="sm" asChild>
                <Link href={`/trips/${trip.id}/manage`}>
                  <Settings className="h-4 w-4" />
                </Link>
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold mb-4">My Trips</h1>
          <p className="text-xl text-muted-foreground">
            Manage your organized trips and view your travel history
          </p>
        </div>
        <Button asChild size="lg">
          <Link href="/trips/create">
            <PlusCircle className="mr-2 h-4 w-4" />
            Create New Trip
          </Link>
        </Button>
      </div>

      {/* Trip Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 text-center">
          <div className="text-2xl font-bold text-primary">
            {organizedTrips.length}
          </div>
          <div className="text-sm text-muted-foreground">Trips Organized</div>
        </Card>
        <Card className="p-4 text-center">
          <div className="text-2xl font-bold text-primary">
            {joinedTrips.length}
          </div>
          <div className="text-sm text-muted-foreground">Trips Joined</div>
        </Card>
        <Card className="p-4 text-center">
          <div className="text-2xl font-bold text-primary">
            {trips.filter(t => t.status === "completed").length}
          </div>
          <div className="text-sm text-muted-foreground">Completed</div>
        </Card>
        <Card className="p-4 text-center">
          <div className="text-2xl font-bold text-primary">
            {trips.filter(t => t.status === "upcoming").length}
          </div>
          <div className="text-sm text-muted-foreground">Upcoming</div>
        </Card>
      </div>

      {/* Trips Tabs */}
      <Tabs defaultValue="organized" className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="organized">
            Organized by Me ({organizedTrips.length})
          </TabsTrigger>
          <TabsTrigger value="joined">
            Joined Trips ({joinedTrips.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="organized" className="space-y-6">
          {organizedTrips.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {organizedTrips.map((trip) => (
                <TripCard key={trip.id} trip={trip} />
              ))}
            </div>
          ) : (
            <Card className="p-12 text-center">
              <div className="space-y-4">
                <MapPin className="h-16 w-16 mx-auto text-muted-foreground" />
                <div>
                  <h3 className="text-xl font-semibold mb-2">No trips organized yet</h3>
                  <p className="text-muted-foreground">
                    Create your first trip and start sharing amazing experiences with others
                  </p>
                </div>
                <Button asChild>
                  <Link href="/trips/create">
                    <PlusCircle className="mr-2 h-4 w-4" />
                    Create Your First Trip
                  </Link>
                </Button>
              </div>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="joined" className="space-y-6">
          {joinedTrips.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {joinedTrips.map((trip) => (
                <TripCard key={trip.id} trip={trip} />
              ))}
            </div>
          ) : (
            <Card className="p-12 text-center">
              <div className="space-y-4">
                <Users className="h-16 w-16 mx-auto text-muted-foreground" />
                <div>
                  <h3 className="text-xl font-semibold mb-2">No trips joined yet</h3>
                  <p className="text-muted-foreground">
                    Browse available trips and join your next adventure
                  </p>
                </div>
                <Button asChild>
                  <Link href="/trips">
                    <MapPin className="mr-2 h-4 w-4" />
                    Browse Trips
                  </Link>
                </Button>
              </div>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
