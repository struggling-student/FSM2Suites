// User types
export interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  cityOfOrigin: string;
  registrationDate: Date;
  rating: number; // 0-5 based on feedback scores
}

// Location types
export interface Location {
  id: string;
  address: string;
  city: string;
  region: string;
  country: string;
}

// Activity types
export type ActivityType = 'visit' | 'meal' | 'tour' | 'transport' | 'overnight_stay';

export interface BaseActivity {
  id: string;
  name: string;
  type: ActivityType;
  startTime: Date;
  duration: number; // in minutes
  price: number;
  location: Location;
  description: string;
  ticketCodes: string[];
  participantIds?: string[]; // if empty, all trip participants join
  isComposite?: boolean;
  subActivities?: BaseActivity[];
}

export interface TransportActivity extends BaseActivity {
  type: 'transport';
  departureLocation: Location;
  arrivalLocation: Location;
}

export interface OvernightStayActivity extends BaseActivity {
  type: 'overnight_stay';
  checkInTime: Date;
  checkOutTime: Date;
}

export type Activity = BaseActivity | TransportActivity | OvernightStayActivity;

// Trip types
export interface Trip {
  id: string;
  name: string;
  minParticipants: number;
  maxParticipants: number;
  organizerId: string;
  organizer: User;
  activities: Activity[];
  participants: User[];
  startDate: Date;
  endDate: Date;
  totalPrice: number;
  destinations: string[]; // cities involved
  createdAt: Date;
}

// Feedback types
export interface Feedback {
  id: string;
  userId: string;
  tripId: string;
  score: number; // 1-5
  comment?: string;
  createdAt: Date;
}

// Search and filter types
export interface TripSearchFilters {
  destination?: string;
  startDate?: Date;
  endDate?: Date;
  minBudget?: number;
  maxBudget?: number;
  regions?: string[];
  minOrganizerRating?: number;
}

export interface TripStatistics {
  city: string;
  month: string;
  year: number;
  tripCount: number;
}

// Form types
export interface CreateTripForm {
  name: string;
  minParticipants: number;
  maxParticipants: number;
  startDate: Date;
  endDate: Date;
}

export interface CreateActivityForm {
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
  ticketCodes: string;
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

export interface UserRegistrationForm {
  firstName: string;
  lastName: string;
  email: string;
  cityOfOrigin: string;
}
