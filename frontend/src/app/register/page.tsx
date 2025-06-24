"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  User, 
  Mail, 
  MapPin,
  ArrowRight,
  Check
} from "lucide-react";
import { toast } from "sonner";

export default function RegisterPage() {
  const router = useRouter();
  
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    cityOfOrigin: "",
    country: ""
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const countries = [
    "Spain", "Italy", "France", "Germany", "Netherlands", 
    "Portugal", "Greece", "Austria", "Belgium", "Switzerland",
    "United Kingdom", "Sweden", "Norway", "Denmark", "Finland"
  ];

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.firstName.trim()) {
      newErrors.firstName = "First name is required";
    }
    
    if (!formData.lastName.trim()) {
      newErrors.lastName = "Last name is required";
    }
    
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address";
    }
    
    if (!formData.cityOfOrigin.trim()) {
      newErrors.cityOfOrigin = "City of origin is required";
    }
    
    if (!formData.country) {
      newErrors.country = "Country is required";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // In a real app, this would make an API call to register the user
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API call
      
      console.log("Registration data:", formData);
      
      toast.success("Registration successful! Welcome to TravelPlan!");
      router.push("/");
    } catch (error) {
      toast.error("Registration failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: "" }));
    }
  };

  const benefits = [
    "Create and organize amazing trips",
    "Join trips organized by verified members",
    "Access to exclusive travel experiences",
    "Connect with fellow travelers",
    "Rate and review trip organizers",
    "Get personalized trip recommendations"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/10 via-background to-secondary/10 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Benefits */}
        <div className="space-y-6">
          <div>
            <h1 className="text-4xl font-bold mb-4">Join TravelPlan</h1>
            <p className="text-xl text-muted-foreground">
              Start your journey with the world's leading travel community
            </p>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">What you'll get:</h3>
            <ul className="space-y-3">
              {benefits.map((benefit, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="bg-primary/10 rounded-full p-1 mt-0.5">
                    <Check className="h-4 w-4 text-primary" />
                  </div>
                  <span className="text-muted-foreground">{benefit}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <div className="pt-4">
            <p className="text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link href="/login" className="text-primary hover:underline">
                Sign in here
              </Link>
            </p>
          </div>
        </div>

        {/* Right side - Registration Form */}
        <Card className="w-full">
          <CardHeader>
            <CardTitle className="text-2xl">Create Your Account</CardTitle>
            <CardDescription>
              Fill in your details to get started with TravelPlan
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name Fields */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name *</Label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="firstName"
                      placeholder="John"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange("firstName", e.target.value)}
                      className={`pl-10 ${errors.firstName ? "border-red-500" : ""}`}
                    />
                  </div>
                  {errors.firstName && (
                    <p className="text-sm text-red-500">{errors.firstName}</p>
                  )}
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name *</Label>
                  <Input
                    id="lastName"
                    placeholder="Doe"
                    value={formData.lastName}
                    onChange={(e) => handleInputChange("lastName", e.target.value)}
                    className={errors.lastName ? "border-red-500" : ""}
                  />
                  {errors.lastName && (
                    <p className="text-sm text-red-500">{errors.lastName}</p>
                  )}
                </div>
              </div>

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email">Email Address *</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="john@example.com"
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    className={`pl-10 ${errors.email ? "border-red-500" : ""}`}
                  />
                </div>
                {errors.email && (
                  <p className="text-sm text-red-500">{errors.email}</p>
                )}
              </div>

              {/* Location */}
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="cityOfOrigin">City of Origin *</Label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="cityOfOrigin"
                      placeholder="Barcelona"
                      value={formData.cityOfOrigin}
                      onChange={(e) => handleInputChange("cityOfOrigin", e.target.value)}
                      className={`pl-10 ${errors.cityOfOrigin ? "border-red-500" : ""}`}
                    />
                  </div>
                  {errors.cityOfOrigin && (
                    <p className="text-sm text-red-500">{errors.cityOfOrigin}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="country">Country *</Label>
                  <Select
                    value={formData.country}
                    onValueChange={(value) => handleInputChange("country", value)}
                  >
                    <SelectTrigger className={errors.country ? "border-red-500" : ""}>
                      <SelectValue placeholder="Select your country" />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.map(country => (
                        <SelectItem key={country} value={country}>
                          {country}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {errors.country && (
                    <p className="text-sm text-red-500">{errors.country}</p>
                  )}
                </div>
              </div>

              {/* Terms and Conditions */}
              <div className="text-sm text-muted-foreground">
                By creating an account, you agree to our{" "}
                <Link href="/terms" className="text-primary hover:underline">
                  Terms of Service
                </Link>{" "}
                and{" "}
                <Link href="/privacy" className="text-primary hover:underline">
                  Privacy Policy
                </Link>
              </div>

              {/* Submit Button */}
              <Button 
                type="submit" 
                className="w-full" 
                size="lg"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  "Creating Account..."
                ) : (
                  <>
                    Create Account
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
