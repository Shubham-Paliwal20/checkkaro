# Frontend: User Corrections System

## Overview

Your backend already has a complete user corrections system. Now you need to add the frontend UI so users can report incorrect AI-generated ingredients.

---

## What's Already Built (Backend)

### ✅ Correction Endpoint
```
POST /api/product/correct
```

**Parameters:**
- `product_name` (string, required)
- `ingredients` (string, required) - correct ingredients list
- `product_id` (string, optional)

**Response:**
```json
{
  "success": true,
  "message": "Thank you! Your correction has been submitted for review.",
  "correction_id": "uuid"
}
```

### ✅ Database Table
`pending_corrections` table stores all user submissions:
- Product name
- Submitted ingredients
- Submission timestamp
- Status (pending/approved/rejected)
- Review notes

---

## What You Need to Build (Frontend)

### 1. "Report Incorrect Ingredients" Button

Add to `Result.jsx` page (where product details are shown):

```jsx
// In Result.jsx
import { useState } from 'react';

function Result() {
  const [showCorrectionModal, setShowCorrectionModal] = useState(false);
  
  return (
    <div>
      {/* Existing product display */}
      
      {/* Add this button near the ingredients section */}
      <div className="mt-4 flex justify-center">
        <button
          onClick={() => setShowCorrectionModal(true)}
          className="flex items-center gap-2 px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          Report Incorrect Ingredients
        </button>
      </div>
      
      {/* Correction Modal */}
      {showCorrectionModal && (
        <CorrectionModal
          productName={productData.name}
          productId={productData.id}
          onClose={() => setShowCorrectionModal(false)}
        />
      )}
    </div>
  );
}
```

---

### 2. Correction Modal Component

Create `src/components/CorrectionModal.jsx`:

```jsx
import { useState } from 'react';

function CorrectionModal({ productName, productId, onClose }) {
  const [ingredients, setIngredients] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null); // 'success' | 'error' | null

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!ingredients.trim()) {
      alert('Please enter the correct ingredients');
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await fetch(
        `http://localhost:8000/api/product/correct?product_name=${encodeURIComponent(productName)}&ingredients=${encodeURIComponent(ingredients)}&product_id=${productId}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      const data = await response.json();

      if (data.success) {
        setSubmitStatus('success');
        setTimeout(() => {
          onClose();
        }, 2000);
      } else {
        setSubmitStatus('error');
      }
    } catch (error) {
      console.error('Error submitting correction:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">
              Report Incorrect Ingredients
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="mt-2 text-sm text-gray-600">
            Product: <span className="font-semibold">{productName}</span>
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Correct Ingredients List
            </label>
            <p className="text-xs text-gray-500 mb-2">
              Please enter the ingredients exactly as they appear on the product label, separated by commas.
            </p>
            <textarea
              value={ingredients}
              onChange={(e) => setIngredients(e.target.value)}
              placeholder="Example: Water, Sodium Lauryl Sulfate, Cocamidopropyl Betaine, Glycerin, Fragrance..."
              className="w-full h-32 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isSubmitting}
            />
          </div>

          {/* Info Box */}
          <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex gap-2">
              <svg className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-800">
                <p className="font-semibold mb-1">How to help:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>Check the product label or packaging</li>
                  <li>List ingredients in the order they appear</li>
                  <li>Include all ingredients, even small amounts</li>
                  <li>Your submission will be reviewed before updating</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Status Messages */}
          {submitStatus === 'success' && (
            <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex gap-2">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <p className="text-sm text-green-800 font-semibold">
                  Thank you! Your correction has been submitted for review.
                </p>
              </div>
            </div>
          )}

          {submitStatus === 'error' && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex gap-2">
                <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <p className="text-sm text-red-800 font-semibold">
                  Error submitting correction. Please try again.
                </p>
              </div>
            </div>
          )}

          {/* Buttons */}
          <div className="flex gap-3 justify-end">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
              disabled={isSubmitting || !ingredients.trim()}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Correction'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CorrectionModal;
```

---

### 3. Confidence Badges

Add confidence indicators to show data source quality.

Create `src/components/ConfidenceBadge.jsx`:

```jsx
function ConfidenceBadge({ dataSource, confidence }) {
  const getBadgeConfig = () => {
    // User verified data (from corrections)
    if (dataSource === 'user_verified') {
      return {
        text: 'User Verified',
        icon: '✓',
        bgColor: 'bg-green-100',
        textColor: 'text-green-800',
        borderColor: 'border-green-300',
      };
    }
    
    // From database cache
    if (dataSource === 'database_cache') {
      return {
        text: 'From Database',
        icon: '📦',
        bgColor: 'bg-blue-100',
        textColor: 'text-blue-800',
        borderColor: 'border-blue-300',
      };
    }
    
    // From external sources (Open Food Facts, BigBasket)
    if (dataSource === 'openfoodfacts' || dataSource === 'bigbasket') {
      return {
        text: 'External Source',
        icon: '🔗',
        bgColor: 'bg-purple-100',
        textColor: 'text-purple-800',
        borderColor: 'border-purple-300',
      };
    }
    
    // AI estimated (low confidence)
    if (dataSource === 'ai_estimated' || confidence === 'low') {
      return {
        text: 'AI Estimated',
        icon: '⚠️',
        bgColor: 'bg-yellow-100',
        textColor: 'text-yellow-800',
        borderColor: 'border-yellow-300',
      };
    }
    
    // Default
    return {
      text: 'Analyzed',
      icon: '🔍',
      bgColor: 'bg-gray-100',
      textColor: 'text-gray-800',
      borderColor: 'border-gray-300',
    };
  };

  const config = getBadgeConfig();

  return (
    <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full border ${config.bgColor} ${config.textColor} ${config.borderColor}`}>
      <span className="text-sm">{config.icon}</span>
      <span className="text-xs font-semibold">{config.text}</span>
    </div>
  );
}

export default ConfidenceBadge;
```

**Usage in Result.jsx:**

```jsx
import ConfidenceBadge from '../components/ConfidenceBadge';

function Result() {
  return (
    <div>
      {/* Product header */}
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">{productData.name}</h1>
        <ConfidenceBadge 
          dataSource={productData.data_source} 
          confidence={productData.confidence} 
        />
      </div>
      
      {/* Rest of product display */}
    </div>
  );
}
```

---

### 4. Warning for AI-Estimated Data

Add a warning banner when data is AI-estimated (low confidence):

```jsx
// In Result.jsx
{productData.data_source === 'ai_estimated' && (
  <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
    <div className="flex gap-3">
      <svg className="w-6 h-6 text-yellow-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <div>
        <h3 className="font-semibold text-yellow-900 mb-1">
          AI-Estimated Ingredients
        </h3>
        <p className="text-sm text-yellow-800 mb-2">
          We couldn't find verified ingredient data for this product. The ingredients shown are estimated by AI and may not be 100% accurate.
        </p>
        <p className="text-sm text-yellow-800">
          Have the actual ingredient list? Please help us improve by reporting the correct ingredients below.
        </p>
      </div>
    </div>
  </div>
)}
```

---

## Implementation Steps

### Step 1: Create CorrectionModal Component
```bash
# Create the file
touch frontend/src/components/CorrectionModal.jsx
```

Copy the modal code above into this file.

### Step 2: Create ConfidenceBadge Component
```bash
# Create the file
touch frontend/src/components/ConfidenceBadge.jsx
```

Copy the badge code above into this file.

### Step 3: Update Result.jsx

Add imports:
```jsx
import { useState } from 'react';
import CorrectionModal from '../components/CorrectionModal';
import ConfidenceBadge from '../components/ConfidenceBadge';
```

Add state:
```jsx
const [showCorrectionModal, setShowCorrectionModal] = useState(false);
```

Add the components to your JSX (see examples above).

### Step 4: Test

1. Search for a product
2. Click "Report Incorrect Ingredients"
3. Fill in correct ingredients
4. Submit
5. Check backend logs for:
   ```
   [PRODUCT CORRECT] New correction submitted for: Product Name
   ```
6. Check database:
   ```sql
   SELECT * FROM pending_corrections ORDER BY submitted_at DESC LIMIT 5;
   ```

---

## Future Enhancements

### Admin Panel (Phase 2)

Create an admin interface to review corrections:

**Features:**
- List all pending corrections
- View submitted ingredients vs current ingredients
- Approve/reject with notes
- Bulk approve similar corrections
- Update cached product when approved

**Endpoint to Add:**
```
POST /api/admin/corrections/{correction_id}/review
```

**Parameters:**
- `status` (approved/rejected)
- `notes` (optional)

**Logic:**
1. Update correction status
2. If approved, update cached product
3. Re-analyze with new ingredients
4. Update product_ingredients table

### Confidence Scoring (Phase 3)

Track data quality:
- User verified: 100% confidence
- External source: 80% confidence
- AI estimated: 40% confidence
- Multiple user verifications: Increase confidence

### Voting System (Phase 4)

Let users vote on accuracy:
- "Is this information accurate?" (Yes/No)
- Track votes per product
- Auto-flag products with many "No" votes
- Prioritize for re-analysis

---

## Database Queries for Admin

### View Pending Corrections
```sql
SELECT 
  pc.id,
  pc.product_name,
  pc.submitted_ingredients,
  pc.submitted_at,
  p.name as current_name,
  p.awareness_score as current_score
FROM pending_corrections pc
LEFT JOIN products p ON pc.product_id = p.id
WHERE pc.status = 'pending'
ORDER BY pc.submitted_at DESC;
```

### Count Corrections by Status
```sql
SELECT status, COUNT(*) as count
FROM pending_corrections
GROUP BY status;
```

### Most Corrected Products
```sql
SELECT product_name, COUNT(*) as correction_count
FROM pending_corrections
GROUP BY product_name
ORDER BY correction_count DESC
LIMIT 10;
```

---

## Summary

### What You're Building

1. ✅ **Report Button** - Easy access on Result page
2. ✅ **Correction Modal** - User-friendly form
3. ✅ **Confidence Badges** - Show data source quality
4. ✅ **Warning Banner** - Alert for AI-estimated data
5. ⏳ **Admin Panel** - Review and approve (future)

### User Flow

1. User searches product
2. Sees AI-estimated ingredients
3. Notices they're incorrect
4. Clicks "Report Incorrect Ingredients"
5. Enters correct ingredients from label
6. Submits correction
7. Correction saved to database
8. Admin reviews and approves
9. Product cache updated
10. Future users see correct data

### Benefits

- **Crowdsourced accuracy** - Users help improve data
- **Build trust** - Show transparency about data sources
- **Continuous improvement** - Database gets better over time
- **Community engagement** - Users feel involved

---

## Next Steps

1. ✅ Run SQL migration (from URGENT_ACTION_REQUIRED.md)
2. ✅ Test caching works
3. 🔨 Create CorrectionModal component
4. 🔨 Create ConfidenceBadge component
5. 🔨 Update Result.jsx
6. 🔨 Test correction submission
7. 📊 Monitor corrections in database
8. 🚀 Build admin panel (future)

---

**Start with the modal and badge components - they're independent and easy to test!** 🎨
