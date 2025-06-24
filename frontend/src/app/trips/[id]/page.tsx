"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  MapPin, 
  Users, 
  Calendar as CalendarIcon, 
  Star, 
  Clock,
  DollarSign,
  User,
  MessageCircle,
  Share2,
  Heart,
  ArrowLeft
} from "lucide-react";
import { toast } from "sonner";

export default function TripDetailPage() {
  const params = useParams();
  const tripId = params.id as string;
  
  const [isJoined, setIsJoined] = useState(false);
  const [isLiked, setIsLiked] = useState(false);

  // Mock trip data - in real app, this would be fetched based on tripId
  const trip = {
    id: tripId,
    name: "Mediterranean Adventure",
    destinations: ["Barcelona", "Rome", "Athens"],
    startDate: "2025-07-15",
    endDate: "2025-07-25",
    price: 1299,
    participants: 8,
    maxParticipants: 12,
    organizer: {
      id: "org1",
      name: "Sarah Johnson",
      rating: 4.8,
      tripsOrganized: 12,
      avatar: "SJ"
    },
    regions: ["Spain", "Italy", "Greece"],
    description: "Embark on an unforgettable journey through the heart of the Mediterranean. This carefully curated adventure combines ancient history, stunning architecture, delicious cuisine, and breathtaking coastlines. From the vibrant streets of Barcelona to the eternal city of Rome, and finally to the cradle of democracy in Athens, each destination offers unique experiences that will create lasting memories.",
    highlights: [
      "Guided tour of Sagrada Familia and Park Güell in Barcelona",
      "Private cooking class with local chef in Rome",
      "Sunset visit to the Acropolis in Athens",
      "Ferry ride through the Greek islands",
      "Wine tasting in Tuscany countryside"
    ],
    activities: [
      {
        id: "1",
        name: "Arrival in Barcelona",
        type: "transport",
        date: "2025-07-15",
        time: "14:00",
        duration: 120,
        price: 0,
        location: "Barcelona Airport",
        description: "Meet at Barcelona Airport for group transfer to hotel"
      },
      {
        id: "2",
        name: "Sagrada Familia Tour",
        type: "visit",
        date: "2025-07-16",
        time: "10:00",
        duration: 180,
        price: 45,
        location: "Sagrada Familia, Barcelona",
        description: "Skip-the-line guided tour of Gaudí's masterpiece"
      },
      {
        id: "3",
        name: "Tapas Walking Tour",
        type: "meal",
        date: "2025-07-16",
        time: "19:00",
        duration: 150,
        price: 65,
        location: "Gothic Quarter, Barcelona",
        description: "Authentic tapas experience in historic Barcelona"
      },
      {
        id: "4",
        name: "High-Speed Train to Rome",
        type: "transport",
        date: "2025-07-18",
        time: "08:00",
        duration: 480,
        price: 280,
        location: "Barcelona to Rome",
        description: "Comfortable high-speed train journey"
      },
      {
        id: "5",
        name: "Colosseum & Roman Forum",
        type: "tour",
        date: "2025-07-19",
        time: "09:00",
        duration: 240,
        price: 55,
        location: "Colosseum, Rome",
        description: "Guided tour with skip-the-line access"
      }
    ],
    feedback: [
      {
        id: "1",
        user: "Mike Chen",
        rating: 5,
        comment: "Absolutely incredible trip! Sarah's organization was flawless and every detail was perfectly planned.",
        date: "2024-09-15"
      },
      {
        id: "2", 
        user: "Emma Rodriguez",
        rating: 5,
        comment: "Best travel experience I've ever had. The mix of culture, food, and adventure was perfect.",
        date: "2024-09-12"
      },
      {
        id: "3",
        user: "James Wilson",
        rating: 4,
        comment: "Great trip overall. Minor timing issues but Sarah handled them professionally.",
        date: "2024-09-10"
      }
    ]
  };

  const handleJoinTrip = () => {
    setIsJoined(true);
    toast.success("Successfully joined the trip! You'll receive confirmation details soon.");
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    toast.success("Trip link copied to clipboard!");
  };

  const handleLike = () => {
    setIsLiked(!isLiked);
    toast.success(isLiked ? "Removed from favorites" : "Added to favorites");
  };

  const getActivityTypeColor = (type: string) => {
    const colors = {
      visit: "bg-blue-100 text-blue-800",
      meal: "bg-orange-100 text-orange-800", 
      tour: "bg-green-100 text-green-800",
      transport: "bg-purple-100 text-purple-800",
      overnight_stay: "bg-indigo-100 text-indigo-800"
    };
    return colors[type as keyof typeof colors] || "bg-gray-100 text-gray-800";
  };

  const availableSpots = trip.maxParticipants - trip.participants;

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Back Button */}
      <Button variant="ghost" asChild>
        <Link href="/trips">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Trips
        </Link>
      </Button>

      {/* Header */}
      <div className="space-y-6">
        <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-6">
          <div className="space-y-4">
            <h1 className="text-4xl font-bold">{trip.name}</h1>
            <div className="flex items-center gap-4 text-muted-foreground">
              <div className="flex items-center gap-1">
                <MapPin className="h-4 w-4" />
                {trip.destinations.join(" → ")}
              </div>
              <div className="flex items-center gap-1">
                <CalendarIcon className="h-4 w-4" />
                {new Date(trip.startDate).toLocaleDateString()} - {new Date(trip.endDate).toLocaleDateString()}
              </div>
            </div>
            <div className="flex items-center gap-2">
              {trip.regions.map(region => (
                <Badge key={region} variant="outline">
                  {region}
                </Badge>
              ))}
            </div>
          </div>

          <div className="flex flex-col lg:items-end gap-4">
            <div className="text-3xl font-bold text-primary">
              ${trip.price}
            </div>
            <div className="flex items-center gap-2">
              <Button onClick={handleShare} variant="outline" size="sm">
                <Share2 className="h-4 w-4" />
              </Button>
              <Button
                onClick={handleLike}
                variant="outline"
                size="sm"
                className={isLiked ? "text-red-500 border-red-200" : ""}
              >
                <Heart className={`h-4 w-4 ${isLiked ? "fill-current" : ""}`} />
              </Button>
              {!isJoined ? (
                <Button onClick={handleJoinTrip} size="lg" disabled={availableSpots === 0}>
                  {availableSpots === 0 ? "Trip Full" : `Join Trip (${availableSpots} spots left)`}
                </Button>
              ) : (
                <Button variant="outline" size="lg" disabled>
                  ✓ Joined
                </Button>
              )}
            </div>
          </div>
        </div>

        {/* Trip Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-4 text-center">
            <Users className="h-6 w-6 mx-auto mb-2 text-primary" />
            <div className="text-2xl font-bold">{trip.participants}</div>
            <div className="text-sm text-muted-foreground">/ {trip.maxParticipants} participants</div>
          </Card>
          <Card className="p-4 text-center">
            <Clock className="h-6 w-6 mx-auto mb-2 text-primary" />
            <div className="text-2xl font-bold">
              {Math.ceil((new Date(trip.endDate).getTime() - new Date(trip.startDate).getTime()) / (1000 * 60 * 60 * 24))}
            </div>
            <div className="text-sm text-muted-foreground">days</div>
          </Card>
          <Card className="p-4 text-center">
            <MapPin className="h-6 w-6 mx-auto mb-2 text-primary" />
            <div className="text-2xl font-bold">{trip.activities.length}</div>
            <div className="text-sm text-muted-foreground">activities</div>
          </Card>
          <Card className="p-4 text-center">
            <Star className="h-6 w-6 mx-auto mb-2 text-primary" />
            <div className="text-2xl font-bold">{trip.organizer.rating}</div>
            <div className="text-sm text-muted-foreground">organizer rating</div>
          </Card>
        </div>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="itinerary">Itinerary</TabsTrigger>
          <TabsTrigger value="organizer">Organizer</TabsTrigger>
          <TabsTrigger value="reviews">Reviews</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>About This Trip</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground leading-relaxed">
                {trip.description}
              </p>
              
              <Separator />
              
              <div>
                <h4 className="font-semibold mb-3">Trip Highlights</h4>
                <ul className="space-y-2">
                  {trip.highlights.map((highlight, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <Star className="h-4 w-4 mt-1 text-primary flex-shrink-0" />
                      <span className="text-muted-foreground">{highlight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="itinerary" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Detailed Itinerary</CardTitle>
              <CardDescription>
                All activities planned for this trip
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {trip.activities.map((activity) => (
                  <div key={activity.id} className="flex gap-4 p-4 border rounded-lg">
                    <div className="text-center min-w-[80px]">
                      <div className="text-sm font-medium">
                        {new Date(activity.date).toLocaleDateString(undefined, { 
                          month: 'short', 
                          day: 'numeric' 
                        })}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {activity.time}
                      </div>
                    </div>
                    
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center gap-2">
                        <h4 className="font-semibold">{activity.name}</h4>
                        <Badge className={getActivityTypeColor(activity.type)}>
                          {activity.type.replace("_", " ")}
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          {activity.duration} minutes
                        </div>
                        <div className="flex items-center gap-1">
                          <DollarSign className="h-4 w-4" />
                          ${activity.price}
                        </div>
                        <div className="flex items-center gap-1">
                          <MapPin className="h-4 w-4" />
                          {activity.location}
                        </div>
                      </div>
                      
                      <p className="text-sm text-muted-foreground">
                        {activity.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="organizer" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Meet Your Organizer</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-start gap-4">
                <Avatar className="h-16 w-16">
                  <AvatarFallback className="text-lg">
                    {trip.organizer.avatar}
                  </AvatarFallback>
                </Avatar>
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold">{trip.organizer.name}</h3>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Star className="h-4 w-4 fill-current text-yellow-500" />
                      {trip.organizer.rating} rating
                    </div>
                    <div className="flex items-center gap-1">
                      <User className="h-4 w-4" />
                      {trip.organizer.tripsOrganized} trips organized
                    </div>
                  </div>
                </div>
              </div>
              
              <Separator />
              
              <div className="space-y-4">
                <h4 className="font-semibold">About the Organizer</h4>
                <p className="text-muted-foreground">
                  Sarah is a passionate travel enthusiast with over 5 years of experience organizing group trips. 
                  She specializes in cultural immersion experiences and has a deep knowledge of Mediterranean 
                  destinations. Her attention to detail and local connections ensure authentic and memorable 
                  experiences for all participants.
                </p>
              </div>
              
              <Button variant="outline" className="w-full">
                <MessageCircle className="mr-2 h-4 w-4" />
                Contact Organizer
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reviews" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Reviews & Feedback</CardTitle>
              <CardDescription>
                What participants say about this organizer's trips
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {trip.feedback.map((review) => (
                <div key={review.id} className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Avatar className="h-8 w-8">
                        <AvatarFallback>
                          {review.user.split(" ").map(n => n[0]).join("")}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <div className="font-medium">{review.user}</div>
                        <div className="text-xs text-muted-foreground">
                          {new Date(review.date).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`h-4 w-4 ${
                            i < review.rating
                              ? "fill-current text-yellow-500"
                              : "text-gray-300"
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                  <p className="text-muted-foreground text-sm leading-relaxed ml-10">
                    {review.comment}
                  </p>
                  {review.id !== trip.feedback[trip.feedback.length - 1].id && (
                    <Separator className="ml-10" />
                  )}
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
