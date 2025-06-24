"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Badge } from "@/components/ui/badge";
import { 
  CalendarIcon, 
  Plus, 
  Trash2, 
  MapPin, 
  Clock, 
  DollarSign,
  Users,
  Save
} from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { toast } from "sonner";
import { ActivityType } from "@/types";

interface Activity {
  id: string;
  name: string;
  type: ActivityType;
  startTime: Date;
  duration: number;
  price: number;
  location: {
    address: string;
    city: string;
    region: string;
    country: string;
  };
  description: string;
  ticketCodes: string[];
  departureLocation?: {
    address: string;
    city: string;
    region: string;
    country: string;
  };
  arrivalLocation?: {
    address: string;
    city: string;
    region: string;
    country: string;
  };
}

export default function CreateTripPage() {
  const router = useRouter();
  
  // Trip basic info
  const [tripName, setTripName] = useState("");
  const [minParticipants, setMinParticipants] = useState(2);
  const [maxParticipants, setMaxParticipants] = useState(10);
  const [startDate, setStartDate] = useState<Date>();
  const [endDate, setEndDate] = useState<Date>();
  
  // Activities
  const [activities, setActivities] = useState<Activity[]>([]);
  const [showActivityForm, setShowActivityForm] = useState(false);
  
  // Current activity form
  const [currentActivity, setCurrentActivity] = useState<Partial<Activity>>({
    name: "",
    type: "visit",
    duration: 60,
    price: 0,
    location: {
      address: "",
      city: "",
      region: "",
      country: ""
    },
    description: "",
    ticketCodes: []
  });

  const activityTypes: { value: ActivityType; label: string }[] = [
    { value: "visit", label: "Visit" },
    { value: "meal", label: "Meal" },
    { value: "tour", label: "Tour" },
    { value: "transport", label: "Transport" },
    { value: "overnight_stay", label: "Overnight Stay" }
  ];

  const addActivity = () => {
    if (!currentActivity.name || !currentActivity.startTime) {
      toast.error("Please fill in required activity fields");
      return;
    }

    const newActivity: Activity = {
      id: Math.random().toString(36).substr(2, 9),
      name: currentActivity.name!,
      type: currentActivity.type!,
      startTime: currentActivity.startTime!,
      duration: currentActivity.duration || 60,
      price: currentActivity.price || 0,
      location: currentActivity.location!,
      description: currentActivity.description || "",
      ticketCodes: currentActivity.ticketCodes || [],
      ...(currentActivity.type === "transport" && {
        departureLocation: currentActivity.departureLocation,
        arrivalLocation: currentActivity.arrivalLocation
      })
    };

    setActivities([...activities, newActivity]);
    setCurrentActivity({
      name: "",
      type: "visit",
      duration: 60,
      price: 0,
      location: {
        address: "",
        city: "",
        region: "",
        country: ""
      },
      description: "",
      ticketCodes: []
    });
    setShowActivityForm(false);
    toast.success("Activity added successfully");
  };

  const removeActivity = (id: string) => {
    setActivities(activities.filter(activity => activity.id !== id));
    toast.success("Activity removed");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!tripName || !startDate || !endDate || activities.length === 0) {
      toast.error("Please fill in all required fields and add at least one activity");
      return;
    }

    if (startDate >= endDate) {
      toast.error("End date must be after start date");
      return;
    }

    if (minParticipants >= maxParticipants) {
      toast.error("Maximum participants must be greater than minimum participants");
      return;
    }

    // Here you would typically send the data to your backend
    console.log({
      tripName,
      minParticipants,
      maxParticipants,
      startDate,
      endDate,
      activities
    });

    toast.success("Trip created successfully!");
    router.push("/my-trips");
  };

  const totalPrice = activities.reduce((sum, activity) => sum + activity.price, 0);

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Create New Trip</h1>
        <p className="text-xl text-muted-foreground">
          Plan an amazing travel experience for your community
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Basic Trip Information */}
        <Card>
          <CardHeader>
            <CardTitle>Trip Details</CardTitle>
            <CardDescription>
              Basic information about your trip
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="tripName">Trip Name *</Label>
              <Input
                id="tripName"
                placeholder="e.g., Mediterranean Adventure"
                value={tripName}
                onChange={(e) => setTripName(e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="minParticipants">Minimum Participants</Label>
                <Input
                  id="minParticipants"
                  type="number"
                  min="1"
                  value={minParticipants}
                  onChange={(e) => setMinParticipants(parseInt(e.target.value))}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="maxParticipants">Maximum Participants</Label>
                <Input
                  id="maxParticipants"
                  type="number"
                  min="2"
                  value={maxParticipants}
                  onChange={(e) => setMaxParticipants(parseInt(e.target.value))}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Start Date *</Label>
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
                      {startDate ? format(startDate, "PPP") : "Pick start date"}
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
                <Label>End Date *</Label>
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
                      {endDate ? format(endDate, "PPP") : "Pick end date"}
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
            </div>
          </CardContent>
        </Card>

        {/* Activities Section */}
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle>Activities</CardTitle>
                <CardDescription>
                  Add activities for your trip ({activities.length} activities, ${totalPrice} total)
                </CardDescription>
              </div>
              <Button
                type="button"
                onClick={() => setShowActivityForm(true)}
                variant="outline"
              >
                <Plus className="mr-2 h-4 w-4" />
                Add Activity
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Activities List */}
            {activities.length > 0 && (
              <div className="space-y-4">
                {activities.map((activity) => (
                  <Card key={activity.id} className="p-4">
                    <div className="flex justify-between items-start">
                      <div className="space-y-2 flex-1">
                        <div className="flex items-center gap-2">
                          <h4 className="font-semibold">{activity.name}</h4>
                          <Badge variant="secondary">
                            {activityTypes.find(t => t.value === activity.type)?.label}
                          </Badge>
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Clock className="h-4 w-4" />
                            {activity.duration} min
                          </div>
                          <div className="flex items-center gap-1">
                            <DollarSign className="h-4 w-4" />
                            ${activity.price}
                          </div>
                          <div className="flex items-center gap-1">
                            <MapPin className="h-4 w-4" />
                            {activity.location.city}
                          </div>
                          <div className="flex items-center gap-1">
                            <CalendarIcon className="h-4 w-4" />
                            {format(activity.startTime, "PPP")}
                          </div>
                        </div>
                        {activity.description && (
                          <p className="text-sm text-muted-foreground">
                            {activity.description}
                          </p>
                        )}
                      </div>
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => removeActivity(activity.id)}
                        className="text-destructive hover:text-destructive"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            )}

            {/* Activity Form */}
            {showActivityForm && (
              <Card className="p-6 bg-muted/30">
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <h4 className="font-semibold">Add New Activity</h4>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowActivityForm(false)}
                    >
                      Cancel
                    </Button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Activity Name *</Label>
                      <Input
                        placeholder="e.g., Visit Sagrada Familia"
                        value={currentActivity.name}
                        onChange={(e) => setCurrentActivity({
                          ...currentActivity,
                          name: e.target.value
                        })}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label>Activity Type</Label>
                      <Select
                        value={currentActivity.type}
                        onValueChange={(value: ActivityType) => 
                          setCurrentActivity({...currentActivity, type: value})
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {activityTypes.map(type => (
                            <SelectItem key={type.value} value={type.value}>
                              {type.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label>Start Time *</Label>
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button
                            variant="outline"
                            className={cn(
                              "w-full justify-start text-left font-normal",
                              !currentActivity.startTime && "text-muted-foreground"
                            )}
                          >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {currentActivity.startTime ? 
                              format(currentActivity.startTime, "PPP") : 
                              "Pick date"
                            }
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0">
                          <Calendar
                            mode="single"
                            selected={currentActivity.startTime}
                            onSelect={(date) => setCurrentActivity({
                              ...currentActivity,
                              startTime: date
                            })}
                            initialFocus
                          />
                        </PopoverContent>
                      </Popover>
                    </div>

                    <div className="space-y-2">
                      <Label>Duration (minutes)</Label>
                      <Input
                        type="number"
                        min="15"
                        step="15"
                        value={currentActivity.duration}
                        onChange={(e) => setCurrentActivity({
                          ...currentActivity,
                          duration: parseInt(e.target.value)
                        })}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label>Price ($)</Label>
                      <Input
                        type="number"
                        min="0"
                        step="0.01"
                        value={currentActivity.price}
                        onChange={(e) => setCurrentActivity({
                          ...currentActivity,
                          price: parseFloat(e.target.value)
                        })}
                      />
                    </div>
                  </div>

                  {/* Location */}
                  <div className="space-y-4">
                    <Label>Location</Label>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Input
                        placeholder="Address"
                        value={currentActivity.location?.address}
                        onChange={(e) => setCurrentActivity({
                          ...currentActivity,
                          location: { ...currentActivity.location!, address: e.target.value }
                        })}
                      />
                      <Input
                        placeholder="City"
                        value={currentActivity.location?.city}
                        onChange={(e) => setCurrentActivity({
                          ...currentActivity,
                          location: { ...currentActivity.location!, city: e.target.value }
                        })}
                      />
                      <Input
                        placeholder="Region"
                        value={currentActivity.location?.region}
                        onChange={(e) => setCurrentActivity({
                          ...currentActivity,
                          location: { ...currentActivity.location!, region: e.target.value }
                        })}
                      />
                      <Input
                        placeholder="Country"
                        value={currentActivity.location?.country}
                        onChange={(e) => setCurrentActivity({
                          ...currentActivity,
                          location: { ...currentActivity.location!, country: e.target.value }
                        })}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Description</Label>
                    <Textarea
                      placeholder="Describe this activity..."
                      value={currentActivity.description}
                      onChange={(e) => setCurrentActivity({
                        ...currentActivity,
                        description: e.target.value
                      })}
                    />
                  </div>

                  <Button
                    type="button"
                    onClick={addActivity}
                    className="w-full"
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    Add Activity
                  </Button>
                </div>
              </Card>
            )}

            {activities.length === 0 && (
              <div className="text-center py-8 text-muted-foreground">
                <MapPin className="h-16 w-16 mx-auto mb-4 opacity-20" />
                <p>No activities added yet. Add your first activity to get started!</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Submit Button */}
        <div className="flex justify-end space-x-4">
          <Button 
            type="button" 
            variant="outline"
            onClick={() => router.back()}
          >
            Cancel
          </Button>
          <Button type="submit" size="lg">
            <Save className="mr-2 h-4 w-4" />
            Create Trip
          </Button>
        </div>
      </form>
    </div>
  );
}
