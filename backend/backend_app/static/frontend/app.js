// app theme colors
var appTheme = {
    themes: {
        light: {
            base: "#37353a",
            primary: '#673ab7',
            secondary: '#4527a0',
            tertiary: '#b39ddb',
            accent: '#512da8',
        }
    }
};
var appData = {
    theme: appTheme
};
var API_BASE_URL = "";
new Vue({
  el: '#app',
  vuetify: new Vuetify(appData),
  data: function() {
    return {
            apiURL: API_BASE_URL + "/Patient",
            //apiURL: "./data/data.json", for mock data
            initialized: false,
            alert: false,
            dialog: false,
            search: '',
            first_name: "",
            last_name: "",
            gender: "",
            birthdate: "",
            loading: false,
            sortBy: 'last_name',
            headers: [

                {
                    "text": "Last Name",
                    "value": "last_name",
                    filter: value => {
                        if (!this.last_name) return true;
                        return String(value).toLowerCase().indexOf(String(this.last_name).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "First Name",
                    "value": "first_name",
                    filter: value => {
                        if (!this.first_name) return true;
                        return String(value).toLowerCase().indexOf(String(this.first_name).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "Birth Date",
                    "value": "birthdate",
                    filter: value => {
                        if (!this.birthdate) return true;
                        return String(value).toLowerCase().indexOf(String(this.birthdate).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "Gender",
                    "value": "gender",
                    filter: value => {
                        if (!this.gender) return true;
                        return String(value).toLowerCase() === String(this.gender).toLowerCase();
                    },
                    "align": "center"
                },
                {
                    "text": "View Reports",
                    "value": "link",
                    filter: false,
                    "align": "center"
                },
            ],
            results: [],
            errorMessage: ""
        }
    },
    mounted: function() {
        var self = this;
        self.sendRequest(this.apiURL).then(function(response) {
            if (response) {
                var responseObj = JSON.parse(response);
                if (responseObj.patients) {
                    self.results = responseObj.patients;
                    self.results = responseObj.patients.map(function(item) {
                        item["link"] = "";
                        item["EICRLink"] = API_BASE_URL+"/static/"+item.uuid+"_eICR.html";
                        item["RRLink"] = API_BASE_URL+"/static/"+item.uuid+"_RR.html";
                        item["birthdate"] = self.formatBirthDate(item["birthdate"]);
                        return item;
                    });
                }
                //console.log("self.results ", self.results)
            }
            if (!self.results || !self.results.length) {
                self.setError("No data returned from the server.");
                self.initialized = true;
            }
            setTimeout(function(){
                self.initialized = true;
            }.bind(self), 150);
        }).catch(function(e) {
            self.initialized = true;
            self.setError("Unable to display data. see console for detail. " + (e.status && e.statusText ? (e.status + " " + e.statusText): e));
            console.log("api error ", e)
        });
    },
    methods: {
        setError: function(message) {
            if (message) {
                this.errorMessage = message;
                this.alert = true;
                return;
            }
            this.alert = false;
        },
        formatBirthDate: function(dobString) {
            if (!dobString) return "";
            var year = dobString.substr(0, 4);
            var month = dobString.substr(4, 2) - 1;
            var day = dobString.substr(6, 2);
            return year+"-"+month+"-"+day;
        },
        sendRequest: function(url, params) {
            params = params || {};
            // Return a new promise.
            return new Promise(function(resolve, reject) {
              // Do the usual XHR stuff
              var req = new XMLHttpRequest();
              req.open('GET', url);
              req.onload = function() {
                // This is called even on 404 etc
                // so check the status
                if (req.status == 200) {
                  // Resolve the promise with the response text
                  resolve(req.response);
                }
                else {
                  // Otherwise reject with the status text
                  // reject with error, which will hopefully be a meaningful message
                  reject(req);
                }
              };

              // Handle network errors
              req.onerror = function() {
                reject(Error("Network Error"));
              };

              // Make the request
              req.send();
            });
        }
    }
});
