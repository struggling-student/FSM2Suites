"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { 
  BarChart3, 
  TrendingUp, 
  MapPin, 
  Calendar,
  Users,
  Globe,
  Star
} from "lucide-react";

export default function StatisticsPage() {
  const [selectedCity, setSelectedCity] = useState("Barcelona");
  const [selectedCountry, setSelectedCountry] = useState("Spain");
  const [selectedYear, setSelectedYear] = useState("2024");

  // Mock data for statistics
  const cityMonthlyStats = [
    { month: "January", year: 2024, tripCount: 12 },
    { month: "February", year: 2024, tripCount: 15 },
    { month: "March", year: 2024, tripCount: 18 },
    { month: "April", year: 2024, tripCount: 22 },
    { month: "May", year: 2024, tripCount: 28 },
    { month: "June", year: 2024, tripCount: 35 },
    { month: "July", year: 2024, tripCount: 42 },
    { month: "August", year: 2024, tripCount: 38 },
    { month: "September", year: 2024, tripCount: 31 },
    { month: "October", year: 2024, tripCount: 25 },
    { month: "November", year: 2024, tripCount: 19 },
    { month: "December", year: 2024, tripCount: 16 }
  ];

  const mostVisitedCities = [
    { city: "Barcelona", country: "Spain", visits: 145, rank: 1 },
    { city: "Rome", country: "Italy", visits: 132, rank: 2 },
    { city: "Paris", country: "France", visits: 128, rank: 3 },
    { city: "Amsterdam", country: "Netherlands", visits: 98, rank: 4 },
    { city: "Prague", country: "Czech Republic", visits: 87, rank: 5 },
    { city: "Vienna", country: "Austria", visits: 76, rank: 6 },
    { city: "Lisbon", country: "Portugal", visits: 69, rank: 7 },
    { city: "Athens", country: "Greece", visits: 63, rank: 8 },
    { city: "Munich", country: "Germany", visits: 58, rank: 9 },
    { city: "Stockholm", country: "Sweden", visits: 52, rank: 10 }
  ];

  const regionalStats = [
    { region: "Catalonia", country: "Spain", tripCount: 89, timeframe: "2024" },
    { region: "Lazio", country: "Italy", tripCount: 76, timeframe: "2024" },
    { region: "Île-de-France", country: "France", tripCount: 65, timeframe: "2024" },
    { region: "North Holland", country: "Netherlands", tripCount: 54, timeframe: "2024" },
    { region: "Bavaria", country: "Germany", tripCount: 43, timeframe: "2024" },
    { region: "Tuscany", country: "Italy", tripCount: 38, timeframe: "2024" },
    { region: "Andalusia", country: "Spain", tripCount: 32, timeframe: "2024" },
    { region: "Attica", country: "Greece", tripCount: 28, timeframe: "2024" }
  ];

  const topOrganizers = [
    { name: "Sarah Johnson", rating: 4.9, tripsOrganized: 24, totalParticipants: 287 },
    { name: "Marco Weber", rating: 4.8, tripsOrganized: 19, totalParticipants: 234 },
    { name: "Ana Silva", rating: 4.7, tripsOrganized: 16, totalParticipants: 198 },
    { name: "Erik Bjornsson", rating: 5.0, tripsOrganized: 12, totalParticipants: 145 },
    { name: "Pierre Dubois", rating: 4.6, tripsOrganized: 15, totalParticipants: 189 }
  ];

  const overallStats = [
    { label: "Total Trips", value: "1,247", icon: MapPin, change: "+12.5%", trend: "up" },
    { label: "Active Users", value: "25,391", icon: Users, change: "+8.2%", trend: "up" },
    { label: "Countries", value: "42", icon: Globe, change: "+3", trend: "up" },
    { label: "Avg. Rating", value: "4.7", icon: Star, change: "+0.1", trend: "up" }
  ];

  const countries = ["Spain", "Italy", "France", "Germany", "Netherlands", "Portugal", "Greece", "Austria"];
  const cities = {
    "Spain": ["Barcelona", "Madrid", "Seville", "Valencia"],
    "Italy": ["Rome", "Florence", "Venice", "Milan"],
    "France": ["Paris", "Lyon", "Nice", "Bordeaux"],
    "Germany": ["Munich", "Berlin", "Hamburg", "Frankfurt"],
    "Netherlands": ["Amsterdam", "Rotterdam", "Utrecht", "The Hague"],
    "Portugal": ["Lisbon", "Porto", "Faro", "Braga"],
    "Greece": ["Athens", "Thessaloniki", "Patras", "Heraklion"],
    "Austria": ["Vienna", "Salzburg", "Innsbruck", "Graz"]
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Travel Statistics</h1>
        <p className="text-xl text-muted-foreground">
          Insights and analytics about travel patterns and popular destinations
        </p>
      </div>

      {/* Overall Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {overallStats.map((stat, index) => (
          <Card key={index} className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
                <div className={`text-xs flex items-center gap-1 mt-1 ${
                  stat.trend === "up" ? "text-green-600" : "text-red-600"
                }`}>
                  <TrendingUp className="h-3 w-3" />
                  {stat.change}
                </div>
              </div>
              <stat.icon className="h-8 w-8 text-primary" />
            </div>
          </Card>
        ))}
      </div>

      {/* City Monthly Statistics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Monthly Trip Statistics by City
          </CardTitle>
          <CardDescription>
            Number of trips organized per month for selected city
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Country</Label>
              <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {countries.map(country => (
                    <SelectItem key={country} value={country}>
                      {country}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>City</Label>
              <Select value={selectedCity} onValueChange={setSelectedCity}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {cities[selectedCountry as keyof typeof cities]?.map(city => (
                    <SelectItem key={city} value={city}>
                      {city}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold">
              Monthly Statistics for {selectedCity}, {selectedCountry} - {selectedYear}
            </h4>
            <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {cityMonthlyStats.map((stat) => (
                <Card key={stat.month} className="p-3 text-center">
                  <div className="text-lg font-bold text-primary">{stat.tripCount}</div>
                  <div className="text-xs text-muted-foreground">{stat.month}</div>
                </Card>
              ))}
            </div>
            <div className="text-sm text-muted-foreground">
              Total trips organized in {selectedCity} during {selectedYear}: {
                cityMonthlyStats.reduce((sum, stat) => sum + stat.tripCount, 0)
              }
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Most Visited Cities */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            Most Visited Cities
          </CardTitle>
          <CardDescription>
            Cities with the highest number of trips in the last year
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Rank</TableHead>
                <TableHead>City</TableHead>
                <TableHead>Country</TableHead>
                <TableHead>Visits</TableHead>
                <TableHead>Popularity</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mostVisitedCities.map((city) => (
                <TableRow key={city.rank}>
                  <TableCell className="font-medium">#{city.rank}</TableCell>
                  <TableCell className="font-medium">{city.city}</TableCell>
                  <TableCell>{city.country}</TableCell>
                  <TableCell>{city.visits}</TableCell>
                  <TableCell>
                    <Badge variant={
                      city.rank <= 3 ? "default" : 
                      city.rank <= 6 ? "secondary" : "outline"
                    }>
                      {city.rank <= 3 ? "Hot" : city.rank <= 6 ? "Popular" : "Rising"}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Regional Statistics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="h-5 w-5" />
            Regional Statistics
          </CardTitle>
          <CardDescription>
            Number of trips organized per region by country
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Region</TableHead>
                <TableHead>Country</TableHead>
                <TableHead>Trip Count</TableHead>
                <TableHead>Timeframe</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {regionalStats.map((region, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{region.region}</TableCell>
                  <TableCell>{region.country}</TableCell>
                  <TableCell>{region.tripCount}</TableCell>
                  <TableCell>{region.timeframe}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Top Organizers */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Top Organizers
          </CardTitle>
          <CardDescription>
            Highest rated organizers with most trips organized
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Organizer</TableHead>
                <TableHead>Rating</TableHead>
                <TableHead>Trips Organized</TableHead>
                <TableHead>Total Participants</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {topOrganizers.map((organizer, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{organizer.name}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Star className="h-4 w-4 fill-current text-yellow-500" />
                      {organizer.rating}
                    </div>
                  </TableCell>
                  <TableCell>{organizer.tripsOrganized}</TableCell>
                  <TableCell>{organizer.totalParticipants}</TableCell>
                  <TableCell>
                    <Badge variant={organizer.rating >= 4.8 ? "default" : "secondary"}>
                      {organizer.rating >= 4.8 ? "Premium" : "Verified"}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
