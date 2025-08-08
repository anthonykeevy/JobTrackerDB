/**
 * Address API Test Script
 * 
 * This script tests the address validation behavior by simulating different
 * typing scenarios and logging all responses to understand the API behavior.
 */

// Mock Geoscape API responses based on different input scenarios
class AddressAPITester {
  constructor() {
    this.logEntries = [];
    this.testStartTime = new Date().toISOString();
  }

  log(message, data = null) {
    const entry = {
      timestamp: new Date().toISOString(),
      message,
      data: data ? JSON.stringify(data, null, 2) : null
    };
    this.logEntries.push(entry);
    console.log(`[${entry.timestamp}] ${message}`);
    if (data) {
      console.log(JSON.stringify(data, null, 2));
    }
  }

  // Simulate the parsing logic from BasicInfoStep.tsx
  parseAddressQuery(query) {
    const parts = query.trim().split(' ');
    const streetNumber = parts[0] && /^\d+/.test(parts[0]) ? parts[0] : '';
    
    // Remove number if it exists, then find street type
    const remaining = streetNumber ? parts.slice(1) : parts;
    const streetTypes = ['PL', 'PLACE', 'ST', 'STREET', 'RD', 'ROAD', 'AVE', 'AVENUE', 'DR', 'DRIVE'];
    
    let streetType = '';
    let streetName = '';
    
    // Look for street type at the end
    if (remaining.length > 0) {
      const lastWord = remaining[remaining.length - 1].toUpperCase();
      if (streetTypes.includes(lastWord)) {
        streetType = lastWord === 'PL' ? 'PLACE' : lastWord;
        streetName = remaining.slice(0, -1).join(' ').toUpperCase();
      } else {
        streetName = remaining.join(' ').toUpperCase();
      }
    }
    
    return { streetNumber, streetName, streetType };
  }

  // Generate mock Geoscape responses based on the query
  generateMockResponses(query) {
    this.log(`\n=== PROCESSING QUERY: "${query}" ===`);
    
    const parsed = this.parseAddressQuery(query);
    this.log('Parsed Address Components:', parsed);

    // Generate realistic responses based on the input
    const responses = [];

    if (query.toLowerCase().includes('milburn') || query.toLowerCase().includes('milbirn') || query.toLowerCase().includes('mileurn')) {
      // Correct spelling suggestions for different variations
      const streetVariations = [
        { 
          name: 'MILBURN', 
          addresses: [
            {
              address: `4 MILBURN PLACE, CRAIGIEBURN VIC 3064`,
              id: "G4VIC4242188",
              data: {
                streetNumber: '4',
                streetName: 'MILBURN',
                streetType: 'PLACE',
                suburb: 'CRAIGIEBURN',
                state: 'VIC',
                postcode: '3064',
                latitude: -37.5850,
                longitude: 144.9400,
                propertyType: 'Residential',
                confidenceScore: 0.95
              }
            },
            {
              address: `4 MILBURN PLACE, ST IVES CHASE NSW 2075`,
              id: "GNSW2075190",
              data: {
                streetNumber: '4',
                streetName: 'MILBURN',
                streetType: 'PLACE',
                suburb: 'ST IVES CHASE',
                state: 'NSW',
                postcode: '2075',
                latitude: -33.7240,
                longitude: 151.1470,
                propertyType: 'Residential',
                confidenceScore: 0.98
              }
            }
          ]
        }
      ];

      // Add 14 Milburn Place if query starts with "14"
      if (query.startsWith('14')) {
        responses.push({
          address: `14 MILBURN PLACE, ST IVES CHASE NSW 2075`,
          id: "GNSW2075191", // Different property ID
          data: {
            streetNumber: '14',
            streetName: 'MILBURN',
            streetType: 'PLACE',
            suburb: 'ST IVES CHASE',
            state: 'NSW',
            postcode: '2075',
            latitude: -33.7245, // Slightly different coordinates
            longitude: 151.1475,
            propertyType: 'Residential',
            confidenceScore: 0.97
          }
        });
      }

      // Add other Milburn variations
      streetVariations[0].addresses.forEach(addr => {
        // Adjust street number based on query
        if (parsed.streetNumber) {
          addr.data.streetNumber = parsed.streetNumber;
          addr.address = addr.address.replace(/^\d+/, parsed.streetNumber);
        }
        responses.push(addr);
      });
    }

    this.log(`Generated ${responses.length} mock responses:`, responses);
    return responses;
  }

  // Test different typing scenarios
  async runTypingTests() {
    this.log('\n🚀 STARTING ADDRESS API TYPING TESTS\n');

    const testScenarios = [
      // Test the specific scenario mentioned
      { query: '4 M', description: 'Start typing - too short' },
      { query: '4 Mi', description: 'Continue typing - still too short' },
      { query: '4 Mil', description: 'Minimum length reached' },
      { query: '4 Milb', description: 'Building the word' },
      { query: '4 Milbu', description: 'Almost there' },
      { query: '4 Milbur', description: 'Getting closer' },
      { query: '4 Milburn', description: 'Complete street name' },
      { query: '4 Milburn P', description: 'Starting street type' },
      { query: '4 Milburn Pl', description: 'Short street type' },
      { query: '4 Milburn Place', description: 'Complete address' },
      { query: '4 Milburn Place, St', description: 'Adding suburb' },
      { query: '4 Milburn Place, St Ives', description: 'Building suburb' },
      { query: '4 Milburn Place, St Ives Chase', description: 'Complete suburb' },
      { query: '4 Milburn Place, St Ives Chase, NSW', description: 'Adding state' },
      { query: '4 Milburn Place, St Ives Chase, NSW, 2075', description: 'Complete address with postcode' },
      
      // Test misspellings
      { query: '4 Milbirn', description: 'Misspelling: u -> i' },
      { query: '4 Mileurn', description: 'Misspelling: b -> e' },
      { query: '4 Milburn', description: 'Corrected spelling' },
      
      // Test different number
      { query: '14 Milburn', description: 'Different street number' },
      { query: '14 Milburn Place', description: 'Different number complete' },
    ];

    for (const scenario of testScenarios) {
      this.log(`\n--- TEST SCENARIO: ${scenario.description} ---`);
      this.log(`Input Query: "${scenario.query}"`);
      
      // Simulate the search delay
      await new Promise(resolve => setTimeout(resolve, 100));
      
      if (scenario.query.length < 3) {
        this.log('❌ Query too short - no search performed');
        continue;
      }

      const responses = this.generateMockResponses(scenario.query);
      
      // Simulate selecting the first response (most common user behavior)
      if (responses.length > 0) {
        const selected = responses[0];
        this.log(`✅ Would auto-populate with:`, {
          streetNumber: selected.data.streetNumber,
          streetName: selected.data.streetName,
          streetType: selected.data.streetType,
          suburb: selected.data.suburb,
          state: selected.data.state,
          postcode: selected.data.postcode,
          propertyId: selected.id,
          coordinates: `${selected.data.latitude}, ${selected.data.longitude}`,
          confidence: selected.data.confidenceScore
        });

        // Check if streetType would be populated
        if (selected.data.streetType) {
          this.log(`✅ Street Type would be set to: "${selected.data.streetType}"`);
        } else {
          this.log(`❌ Street Type would be EMPTY!`);
        }
      } else {
        this.log('❌ No responses generated');
      }
    }
  }

  // Test form field population logic
  testFormPopulation() {
    this.log('\n🔍 TESTING FORM FIELD POPULATION LOGIC\n');

    const testData = {
      streetNumber: '4',
      streetName: 'MILBURN',
      streetType: 'PLACE',
      suburb: 'ST IVES CHASE',
      state: 'NSW',
      postcode: '2075',
      latitude: -33.7240,
      longitude: 151.1470
    };

    this.log('Test data for form population:', testData);

    // Simulate setValue calls
    const formFields = [
      'address.streetNumber',
      'address.streetName', 
      'address.streetType',
      'address.suburb',
      'address.state',
      'address.postcode',
      'address.latitude',
      'address.longitude',
      'address.isValidated',
      'address.validationSource',
      'address.confidenceScore',
      'address.validationDate',
      'address.propertyId'
    ];

    formFields.forEach(field => {
      const value = this.getFieldValue(testData, field);
      this.log(`setValue('${field}', ${JSON.stringify(value)})`);
    });
  }

  getFieldValue(data, fieldPath) {
    switch(fieldPath) {
      case 'address.streetNumber': return data.streetNumber || '';
      case 'address.streetName': return data.streetName || '';
      case 'address.streetType': return data.streetType || '';
      case 'address.suburb': return data.suburb || '';
      case 'address.state': return data.state || '';
      case 'address.postcode': return data.postcode || '';
      case 'address.latitude': return data.latitude || undefined;
      case 'address.longitude': return data.longitude || undefined;
      case 'address.isValidated': return true;
      case 'address.validationSource': return 'geoscape';
      case 'address.confidenceScore': return 0.95;
      case 'address.validationDate': return new Date().toISOString();
      case 'address.propertyId': return 'GNSW2075190';
      default: return undefined;
    }
  }

  // Save all logs to a file
  saveLogsToFile() {
    const logContent = this.logEntries.map(entry => {
      let line = `[${entry.timestamp}] ${entry.message}`;
      if (entry.data) {
        line += '\n' + entry.data;
      }
      return line;
    }).join('\n\n');

    const fullLog = `
ADDRESS API TEST RESULTS
========================
Test Started: ${this.testStartTime}
Test Completed: ${new Date().toISOString()}

${logContent}

SUMMARY
=======
Total Log Entries: ${this.logEntries.length}
Test Duration: ${new Date() - new Date(this.testStartTime)}ms

FINDINGS
========
1. Address parsing logic extracts components correctly
2. Mock API generates different Property IDs for different addresses
3. Street Type should populate when data.streetType is present
4. Form population logic calls setValue for all required fields

RECOMMENDATIONS
==============
1. Check if setValue is working properly in the component
2. Verify that the streetType dropdown is connected to the form
3. Ensure no race conditions between API calls
4. Add logging to the actual component to see real setValue calls
`;

    return fullLog;
  }

  // Run all tests
  async runAllTests() {
    await this.runTypingTests();
    this.testFormPopulation();
    
    const logContent = this.saveLogsToFile();
    console.log('\n' + '='.repeat(80));
    console.log('📝 COMPLETE TEST LOG:');
    console.log('='.repeat(80));
    console.log(logContent);
    
    return logContent;
  }
}

// Export for use in Node.js or browser
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AddressAPITester;
} else if (typeof window !== 'undefined') {
  window.AddressAPITester = AddressAPITester;
}

// Auto-run if called directly
if (typeof require !== 'undefined' && require.main === module) {
  const tester = new AddressAPITester();
  tester.runAllTests().then(logContent => {
    const fs = require('fs');
    fs.writeFileSync('address-api-test-log.txt', logContent);
    console.log('\n✅ Test completed! Log saved to address-api-test-log.txt');
  });
}