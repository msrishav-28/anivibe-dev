# 🚀 New Features - Quick Reference Guide

## 📍 **Navigation**

All new features are accessible via these routes:

```
/reviews          → Manage your reviews and ratings
/mood             → Discover anime by mood
/hidden-gems      → Find underrated masterpieces
/onboarding       → Complete your profile (new users)
/taste-profile    → View your anime personality
```

---

## ⭐ **1. Ratings & Reviews System**

### **How to Use**

#### **Rate an Anime**
1. Go to any anime detail page
2. Click on the rating widget (10 stars)
3. Optionally add a written review
4. Submit - AI will analyze sentiment automatically

#### **View Your Reviews**
1. Navigate to `/reviews`
2. See stats: Total reviews, average score, latest activity
3. Edit or delete your reviews

#### **Components Used**
- `<RatingWidget>` - Interactive 10-star rating
- `<ReviewForm>` - Submit/edit reviews
- `<ReviewCard>` - Display reviews with sentiment
- `<SentimentBadge>` - Shows positive/negative/neutral

---

## 💡 **2. Explainability System**

### **How to Use**

#### **See Why Anime is Recommended**
1. On any anime card, click "Why recommended?"
2. View natural language explanation
3. See confidence score
4. Check matching factors

#### **Switch Explanation Methods**
- **Hybrid**: Combined analysis
- **Collaborative**: Based on similar users
- **Content**: Based on anime features
- **Semantic**: Based on natural language

#### **Components Used**
- `<ExplanationCard>` - Show reasoning
- `<ExplanationModal>` - Detailed popup
- `<ConfidenceBar>` - Visual confidence score
- `<FactorsList>` - Matching factors

---

## 🎭 **3. Mood-Based Discovery**

### **How to Use**

1. Navigate to `/mood`
2. Select your current mood from 8 options:
   - 😊 Happy - Cheerful and uplifting
   - 💖 Romantic - Love and feelings
   - ⚡ Exciting - Action-packed thrills
   - 🧠 Thoughtful - Deep and philosophical
   - ✨ Whimsical - Magical and fantastical
   - ☕ Relaxed - Calm and peaceful
   - 🌙 Dark - Serious and intense
   - ☀️ Optimistic - Hopeful and bright
3. View personalized recommendations matching your mood

#### **API Call**
```typescript
const results = await api.getMoodBasedRecommendations('happy', 20);
```

---

## 💎 **4. Hidden Gems Discovery**

### **How to Use**

1. Navigate to `/hidden-gems`
2. Adjust filters:
   - **Minimum Score**: Quality threshold (6.0 - 9.0)
   - **Max Popularity**: Discovery threshold (1000 - 20000)
3. Click "Apply Filters"
4. Browse hidden masterpieces with special gem badges

#### **What are Hidden Gems?**
- High-quality anime (7.5+ rating)
- Low popularity (< 10,000 members)
- Underrated masterpieces

#### **API Call**
```typescript
const gems = await api.getHiddenGems({
  min_score: 7.5,
  max_popularity: 10000,
  top_k: 24
});
```

---

## 📊 **5. Taste Profile**

### **How to Use**

1. Navigate to `/taste-profile`
2. View your anime personality:
   - **Favorite Genres**: Top 5 with percentages
   - **Viewing Stats**: Average rating, total ratings
   - **Viewing Patterns**: Most active time, binge watcher status
   - **Personality Insights**: AI-generated personality badges

3. Click "Refresh" to update with latest data

#### **Requirements**
- Must have rated at least 5 anime
- Data updates in real-time

#### **API Call**
```typescript
const profile = await api.getTasteProfile();
```

---

## 🚀 **6. Onboarding Flow (New Users)**

### **How to Use**

1. Navigate to `/onboarding` (automatic for new users)
2. **Step 1**: Select experience level
   - New to Anime
   - Some Experience
   - Anime Veteran
   - Anime Expert
3. **Step 2**: Choose genres (minimum 3)
4. **Step 3**: Review and confirm
5. Get personalized cold-start recommendations

#### **API Call**
```typescript
const recommendations = await api.getColdStartRecommendations(10);
```

---

## 🔧 **Integration with Existing Features**

### **Anime Detail Page**
Now includes:
- ✅ Rating widget for user input
- ✅ "Why recommended?" button
- ✅ Review section with sentiment analysis

### **Profile Page**
Now includes:
- ✅ Reviews tab
- ✅ Link to taste profile
- ✅ Review statistics

### **Explore Page**
Now includes:
- ✅ Hidden gems filter option
- ✅ Mood-based sorting

---

## 💻 **Code Examples**

### **Submit a Rating**
```typescript
import { api } from '@/lib/api-client';

const submitRating = async (animeId: number, score: number, reviewText?: string) => {
  try {
    const rating = await api.createRating({
      anime_id: animeId,
      score: score,
      review_text: reviewText
    });
    console.log('Rating submitted:', rating);
  } catch (error) {
    console.error('Failed to submit rating:', error);
  }
};
```

### **Get Explanation**
```typescript
import { api } from '@/lib/api-client';

const getExplanation = async (animeId: number) => {
  try {
    const explanation = await api.explainRecommendation(animeId, 'hybrid');
    console.log('Natural language:', explanation.natural_language);
    console.log('Confidence:', explanation.confidence);
    console.log('Factors:', explanation.factors);
  } catch (error) {
    console.error('Failed to get explanation:', error);
  }
};
```

### **Mood-Based Search**
```typescript
import { api } from '@/lib/api-client';

const searchByMood = async (mood: string) => {
  try {
    const recommendations = await api.getMoodBasedRecommendations(mood, 20);
    console.log(`Found ${recommendations.length} anime for ${mood} mood`);
  } catch (error) {
    console.error('Failed to search by mood:', error);
  }
};
```

### **Find Hidden Gems**
```typescript
import { api } from '@/lib/api-client';

const discoverGems = async () => {
  try {
    const gems = await api.getHiddenGems({
      min_score: 7.5,
      max_popularity: 10000,
      top_k: 24
    });
    console.log(`Discovered ${gems.length} hidden gems`);
  } catch (error) {
    console.error('Failed to discover gems:', error);
  }
};
```

---

## 🎨 **Component Props**

### **RatingWidget**
```typescript
<RatingWidget
  value={8.5}
  onChange={(value) => console.log(value)}
  readonly={false}
  size="md" // 'sm' | 'md' | 'lg'
  showValue={true}
/>
```

### **MoodSelector**
```typescript
<MoodSelector
  selectedMood="happy"
  onMoodChange={(mood) => console.log(mood)}
/>
```

### **ExplanationModal**
```typescript
<ExplanationModal
  animeId={123}
  isOpen={true}
  onClose={() => setIsOpen(false)}
/>
```

### **TasteProfile**
```typescript
<TasteProfile
  profile={{
    favorite_genres: [...],
    preferred_types: [...],
    average_rating: 8.2,
    total_ratings: 150,
    viewing_patterns: {...},
    personality_insights: [...]
  }}
/>
```

---

## 📱 **Mobile Experience**

All new features are **fully responsive**:
- ✅ Touch-optimized rating widget
- ✅ Swipeable mood cards
- ✅ Mobile-friendly modals
- ✅ Responsive grid layouts

---

## 🔐 **Authentication**

### **Protected Routes**
These features require authentication:
- `/reviews` - Must be logged in
- `/taste-profile` - Must be logged in
- `/hidden-gems` - Optional login for personalized results
- `/mood` - Optional login for personalized results

### **Public Routes**
- `/onboarding` - Anyone can access

---

## 🐛 **Troubleshooting**

### **"No reviews yet"**
→ You haven't submitted any reviews. Rate an anime first!

### **"Not enough data for taste profile"**
→ Rate at least 5 anime to generate your profile

### **"No hidden gems found"**
→ Try adjusting the filters (lower min score or higher max popularity)

### **Explanation not loading**
→ Check that the anime has been recommended to you

---

## 🎯 **Best Practices**

### **For Users**
1. ✅ Rate at least 10 anime to get accurate recommendations
2. ✅ Write detailed reviews for better community engagement
3. ✅ Try different moods to discover new genres
4. ✅ Check hidden gems weekly for fresh discoveries
5. ✅ Complete onboarding for best initial experience

### **For Developers**
1. ✅ Always handle loading states
2. ✅ Show error messages clearly
3. ✅ Use TypeScript for type safety
4. ✅ Cache API responses when possible
5. ✅ Test on mobile devices

---

## 📚 **Additional Resources**

- **Full API Documentation**: See `api-client.ts`
- **Component Library**: Browse `/src/components/`
- **Backend Integration**: See `BACKEND_INTEGRATION_COMPLETE.md`
- **Completion Report**: See `COMPLETION_REPORT.md`

---

## 🎉 **Summary**

You now have access to:
- ⭐ **Complete Rating & Review System** with AI sentiment
- 💡 **Explainability System** for understanding recommendations
- 🎭 **Mood-Based Discovery** with 8 emotions
- 💎 **Hidden Gems Finder** for underrated anime
- 📊 **Taste Profile** showing your anime personality
- 🚀 **Onboarding Flow** for new users

**All features are production-ready and fully integrated!** 🚀

---

**Happy anime discovering!** 🎌
