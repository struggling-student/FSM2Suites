"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  MapPin, 
  Users, 
  Calendar, 
  Star, 
  PlusCircle, 
  Search,
  TrendingUp,
  Globe
} from "lucide-react";

export default function HomePage() {
  // Mock data for featured trips
  const featuredTrips = [
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
      image: "/api/placeholder/400/200"
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
      image: "/api/placeholder/400/200"
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
      image: "/api/placeholder/400/200"
    }
  ];

  const features = [
    {
      icon: Users,
      title: "Join Amazing Trips",
      description: "Discover and participate in carefully curated travel experiences organized by trusted members."
    },
    {
      icon: PlusCircle,
      title: "Create Your Trip",
      description: "Plan and organize your own trips with detailed activities, from tours to dining experiences."
    },
    {
      icon: Calendar,
      title: "Smart Planning",
      description: "Intelligent scheduling that considers travel times, activities, and accommodation constraints."
    },
    {
      icon: Star,
      title: "Quality Assurance", 
      description: "Rating system ensures high-quality experiences from organizers with proven track records."
    }
  ];

  const stats = [
    { label: "Active Trips", value: "1,247", icon: MapPin },
    { label: "Happy Travelers", value: "25,391", icon: Users },
    { label: "Countries Covered", value: "89", icon: Globe },
    { label: "Average Rating", value: "4.8", icon: Star }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 text-center bg-gradient-to-br from-primary/10 via-background to-secondary/10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
            Plan Your Perfect Trip
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 leading-relaxed">
            Join amazing travel experiences or create your own. Connect with fellow travelers and explore the world together.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg" className="text-lg px-8 py-6">
              <Link href="/trips">
                <Search className="mr-2 h-5 w-5" />
                Browse Trips
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="text-lg px-8 py-6">
              <Link href="/trips/create">
                <PlusCircle className="mr-2 h-5 w-5" />
                Create Trip
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-muted/30">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-primary/10 rounded-lg mb-4">
                  <stat.icon className="h-6 w-6 text-primary" />
                </div>
                <div className="text-3xl font-bold mb-2">{stat.value}</div>
                <div className="text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Trips */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Featured Trips</h2>
            <p className="text-xl text-muted-foreground">
              Popular destinations and experiences from our top-rated organizers
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredTrips.map((trip) => (
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
                  <CardDescription className="flex items-center gap-1 text-sm">
                    <MapPin className="h-4 w-4" />
                    {trip.destinations.join(" → ")}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between text-sm">
                    <div className="flex items-center gap-1">
                      <Calendar className="h-4 w-4" />
                      {new Date(trip.startDate).toLocaleDateString()}
                    </div>
                    <div className="flex items-center gap-1">
                      <Users className="h-4 w-4" />
                      {trip.participants}/{trip.maxParticipants}
                    </div>
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
          
          <div className="text-center mt-12">
            <Button asChild variant="outline" size="lg">
              <Link href="/trips">
                View All Trips
                <TrendingUp className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-muted/30">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Why Choose TravelPlan?</h2>
            <p className="text-xl text-muted-foreground">
              Everything you need to create and join amazing travel experiences
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center p-6">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-lg mb-6">
                  <feature.icon className="h-8 w-8 text-primary" />
                </div>
                <CardHeader className="p-0 mb-4">
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Start Your Journey?
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Join thousands of travelers who have discovered their perfect trips through TravelPlan
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg" className="text-lg px-8 py-6">
              <Link href="/register">
                Get Started
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="text-lg px-8 py-6">
              <Link href="/trips">
                Explore Trips
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
